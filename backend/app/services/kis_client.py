"""Korea Investment & Securities API client."""

import httpx
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from app.config import settings
from app.services.kis_token_manager import KISTokenManager, KISToken

logger = logging.getLogger(__name__)

# KIS API URLs
KIS_MOCK_URL = "https://openapivts.koreainvestment.com:29443"  # 모의투자
KIS_REAL_URL = "https://openapi.koreainvestment.com:9443"  # 실전투자


class KISClient:
    """Client for interacting with Korea Investment & Securities API."""

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        account_number: str,
        account_code: str,
        trading_mode: str = "MOCK",
        base_url: Optional[str] = None
    ):
        """
        Initialize KIS client.

        Args:
            app_key: KIS API app key
            app_secret: KIS API app secret
            account_number: Trading account number
            account_code: Trading account code
            trading_mode: Trading mode ("MOCK" or "REAL")
            base_url: Optional base URL (overrides trading_mode)
        """
        self.app_key = app_key
        self.app_secret = app_secret
        self.account_number = account_number
        self.account_code = account_code
        self.trading_mode = trading_mode

        # Set base URL based on trading mode
        if base_url:
            self.base_url = base_url
        elif trading_mode == "REAL":
            self.base_url = KIS_REAL_URL
        else:
            self.base_url = KIS_MOCK_URL

        # Initialize token manager for persistent token storage
        self._token_manager = KISTokenManager(app_key=app_key, trading_mode=trading_mode.lower())
        self._access_token: Optional[KISToken] = None

        logger.info(f"[KISClient] Initialized")
        logger.info(f"  - Trading Mode: {trading_mode}")
        logger.info(f"  - Base URL: {self.base_url}")
        logger.info(f"  - Account: {account_number}")

    async def _ensure_token(self) -> None:
        """
        Ensure we have a valid access token.

        Flow:
        1. Check if in-memory token exists and is valid
        2. If not, try to load from file
        3. If file token is invalid/missing, request new token from API
        4. Save new token to file
        """
        # Check in-memory token first
        if self._access_token and not self._access_token.is_expired():
            logger.debug(f"[KISClient] Using in-memory token")
            return

        # Try to load from file
        logger.info(f"[KISClient] Checking for cached token...")
        self._access_token = self._token_manager.load_token()

        if self._access_token:
            logger.info(f"[KISClient] Using cached token from file")
            return

        # Request new token from API
        logger.info(f"[KISClient] No valid cached token, requesting new token...")
        self._access_token = await self._request_new_token()

        # Save to file for future use
        self._token_manager.save_token(self._access_token)

    def _get_headers(self, tr_id: str) -> Dict[str, str]:
        """
        Get request headers with authentication.

        Args:
            tr_id: Transaction ID for the API call

        Returns:
            Dictionary of headers
        """
        return {
            "Content-Type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token.access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": tr_id,
        }

    async def _request_new_token(self) -> KISToken:
        """
        Request new OAuth access token from KIS API.

        Returns:
            KISToken object

        Raises:
            httpx.HTTPStatusError: If API returns error status
            Exception: For other errors
        """
        url = f"{self.base_url}/oauth2/tokenP"
        payload = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
        }

        logger.info(f"[KIS API] Requesting new access token")
        logger.info(f"  - URL: {url}")
        logger.info(f"  - App Key (first 10 chars): {self.app_key[:10]}...")
        logger.info(f"  - App Secret (first 10 chars): {self.app_secret[:10]}...")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)

                logger.info(f"[KIS API] Response Status: {response.status_code}")

                # Log detailed error information
                if response.status_code != 200:
                    logger.error(f"[KIS API] Error Response:")
                    logger.error(f"  - Status: {response.status_code}")
                    logger.error(f"  - Body: {response.text}")
                    logger.error(f"  - Headers: {dict(response.headers)}")

                response.raise_for_status()
                data = response.json()

                logger.info(f"[KIS API] Access token obtained successfully")
                logger.info(f"  - Token Type: {data.get('token_type')}")
                logger.info(f"  - Expires In: {data.get('expires_in')} seconds")

                return KISToken(
                    access_token=data["access_token"],
                    token_type=data["token_type"],
                    expires_in=data["expires_in"],
                    issued_at=datetime.now()
                )
        except httpx.HTTPStatusError as e:
            logger.error(f"[KIS API] HTTP Error: {e.response.status_code}")
            logger.error(f"  - Response: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"[KIS API] Token Error: {type(e).__name__}: {str(e)}")
            logger.error(f"  - URL: {url}")
            logger.error(f"  - App Key (first 10 chars): {self.app_key[:10]}...")
            raise

    async def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance and holdings.

        Returns:
            Dictionary containing account balance information
        """
        await self._ensure_token()

        # 국내주식 잔고조회 API
        url = f"{self.base_url}/uapi/domestic-stock/v1/trading/inquire-balance"

        # TR ID: VTTC8434R (모의투자), TTTC8434R (실전투자)
        tr_id = "VTTC8434R" if self.trading_mode == "MOCK" else "TTTC8434R"
        headers = self._get_headers(tr_id)

        params = {
            "CANO": self.account_number,
            "ACNT_PRDT_CD": self.account_code,
            "AFHR_FLPR_YN": "N",  # 시간외단일가여부
            "OFL_YN": "",  # 오프라인여부
            "INQR_DVSN": "02",  # 조회구분(01:대출일별, 02:종목별)
            "UNPR_DVSN": "01",  # 단가구분
            "FUND_STTL_ICLD_YN": "N",  # 펀드결제분포함여부
            "FNCG_AMT_AUTO_RDPT_YN": "N",  # 융자금액자동상환여부
            "PRCS_DVSN": "00",  # 처리구분(00:전일매매포함, 01:전일매매미포함)
            "CTX_AREA_FK100": "",  # 연속조회검색조건100
            "CTX_AREA_NK100": "",  # 연속조회키100
        }

        logger.info(f"[KIS API] Calling account balance API")
        logger.info(f"  - URL: {url}")
        logger.info(f"  - TR ID: {tr_id}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers, params=params)

            logger.info(f"[KIS API] Balance API Response Status: {response.status_code}")

            if response.status_code != 200:
                logger.error(f"[KIS API] Balance API Error:")
                logger.error(f"  - Status: {response.status_code}")
                logger.error(f"  - Body: {response.text}")

            response.raise_for_status()
            result = response.json()

            # Log response structure for debugging
            logger.info(f"[KIS API] Response structure:")
            logger.info(f"  - Keys: {list(result.keys())}")

            # Log response code and message if present
            if 'rt_cd' in result:
                logger.info(f"  - rt_cd (응답코드): {result['rt_cd']}")
            if 'msg_cd' in result:
                logger.info(f"  - msg_cd (메시지코드): {result['msg_cd']}")
            if 'msg1' in result:
                logger.info(f"  - msg1 (메시지): {result['msg1']}")

            # Log data structure if present
            if 'output1' in result:
                logger.info(f"  - output1 keys: {list(result['output1'].keys()) if isinstance(result['output1'], dict) else 'not a dict'}")
            if 'output2' in result:
                logger.info(f"  - output2 type: {type(result['output2'])}, length: {len(result['output2']) if isinstance(result['output2'], list) else 'not a list'}")

            return result

    async def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price for a stock.

        Args:
            symbol: Stock symbol (e.g., "005930" for Samsung Electronics)

        Returns:
            Dictionary containing current price information
        """
        await self._ensure_token()

        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-price"
        headers = self._get_headers("FHKST01010100")
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

    async def place_order(
        self,
        symbol: str,
        order_type: str,
        quantity: int,
        price: int
    ) -> Dict[str, Any]:
        """
        Place a buy or sell order.

        Args:
            symbol: Stock symbol
            order_type: "buy" or "sell"
            quantity: Number of shares
            price: Price per share

        Returns:
            Dictionary containing order result
        """
        await self._ensure_token()

        # Different TR IDs for buy and sell
        tr_id = "TTTC0802U" if order_type == "buy" else "TTTC0801U"

        url = f"{self.base_url}/uapi/domestic-stock/v1/trading/order-cash"
        headers = self._get_headers(tr_id)
        payload = {
            "CANO": self.account_number,
            "ACNT_PRDT_CD": self.account_code,
            "PDNO": symbol,
            "ORD_DVSN": "00",
            "ORD_QTY": str(quantity),
            "ORD_UNPR": str(price),
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def get_order_history(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get order history.

        Args:
            start_date: Start date in YYYYMMDD format (optional)
            end_date: End date in YYYYMMDD format (optional)

        Returns:
            Dictionary containing order history
        """
        await self._ensure_token()

        if not end_date:
            end_date = datetime.now().strftime("%Y%m%d")
        if not start_date:
            start_date = end_date

        url = f"{self.base_url}/uapi/domestic-stock/v1/trading/inquire-daily-ccld"
        headers = self._get_headers("TTTC8001R")
        params = {
            "CANO": self.account_number,
            "ACNT_PRDT_CD": self.account_code,
            "INQR_STRT_DT": start_date,
            "INQR_END_DT": end_date,
            "SLL_BUY_DVSN_CD": "00",
            "INQR_DVSN": "00",
            "PDNO": "",
            "CCLD_DVSN": "00",
            "ORD_GNO_BRNO": "",
            "ODNO": "",
            "INQR_DVSN_3": "00",
            "INQR_DVSN_1": "",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

    async def get_daily_chart_data(
        self,
        symbol: str,
        period: str = "D",
        adjusted_price: bool = True
    ) -> Dict[str, Any]:
        """
        Get daily (or period-based) chart data for a stock.

        Args:
            symbol: Stock symbol (e.g., "005930" for Samsung Electronics)
            period: Period code - D(일), W(주), M(월)
            adjusted_price: Whether to use adjusted prices (수정주가)

        Returns:
            Dictionary containing chart data with OHLCV information

        Response structure:
            {
                "rt_cd": "0",  # 응답코드 (0: 성공)
                "msg_cd": "...",  # 메시지코드
                "msg1": "...",  # 메시지
                "output1": {  # 종목 기본 정보
                    "prdy_vrss": "...",  # 전일대비
                    "prdy_vrss_sign": "...",  # 전일대비부호
                    ...
                },
                "output2": [  # 일별 시세 배열
                    {
                        "stck_bsop_date": "20231201",  # 주식영업일자
                        "stck_clpr": "70000",  # 주식종가
                        "stck_oprc": "69500",  # 주식시가
                        "stck_hgpr": "71000",  # 주식최고가
                        "stck_lwpr": "69000",  # 주식최저가
                        "acml_vol": "12345678",  # 누적거래량
                        "acml_tr_pbmn": "...",  # 누적거래대금
                        ...
                    },
                    ...
                ]
            }
        """
        await self._ensure_token()

        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"

        # TR ID: FHKST03010100
        headers = self._get_headers("FHKST03010100")

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # 시장 분류 코드 (J: 주식)
            "FID_INPUT_ISCD": symbol,  # 종목코드
            "FID_INPUT_DATE_1": "",  # 조회 시작일자 (공백: 당일부터 100개)
            "FID_INPUT_DATE_2": "",  # 조회 종료일자
            "FID_PERIOD_DIV_CODE": period,  # 기간분류코드 (D/W/M)
            "FID_ORG_ADJ_PRC": "0" if adjusted_price else "1",  # 수정주가 원주가 가격 (0: 수정주가, 1: 원주가)
        }

        logger.info(f"[KIS API] Calling daily chart data API")
        logger.info(f"  - URL: {url}")
        logger.info(f"  - Symbol: {symbol}")
        logger.info(f"  - Period: {period}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers, params=params)

            logger.info(f"[KIS API] Chart Data Response Status: {response.status_code}")

            if response.status_code != 200:
                logger.error(f"[KIS API] Chart Data Error:")
                logger.error(f"  - Status: {response.status_code}")
                logger.error(f"  - Body: {response.text}")

            response.raise_for_status()
            result = response.json()

            # Log response structure
            if 'rt_cd' in result:
                logger.info(f"  - rt_cd: {result['rt_cd']}")
            if 'msg1' in result:
                logger.info(f"  - msg1: {result['msg1']}")
            if 'output2' in result:
                logger.info(f"  - output2 length: {len(result['output2'])}")

            return result

    async def get_minute_chart_data(
        self,
        symbol: str,
        interval: str = "30"
    ) -> Dict[str, Any]:
        """
        Get intraday minute chart data for a stock.

        Args:
            symbol: Stock symbol (e.g., "005930" for Samsung Electronics)
            interval: Minute interval - "1", "3", "5", "10", "30", "60"

        Returns:
            Dictionary containing minute chart data with OHLCV information

        Response structure:
            {
                "rt_cd": "0",
                "msg_cd": "...",
                "msg1": "...",
                "output1": {  # 종목 정보
                    "prdy_vrss": "...",
                    "prdy_vrss_sign": "...",
                    ...
                },
                "output2": [  # 분별 시세 배열
                    {
                        "stck_bsop_date": "20231201",  # 주식영업일자
                        "stck_cntg_hour": "153000",  # 주식체결시간 (HHMMSS)
                        "stck_prpr": "70000",  # 주식현재가
                        "stck_oprc": "69500",  # 주식시가
                        "stck_hgpr": "71000",  # 주식최고가
                        "stck_lwpr": "69000",  # 주식최저가
                        "cntg_vol": "12345",  # 체결거래량
                        "acml_tr_pbmn": "...",  # 누적거래대금
                        ...
                    },
                    ...
                ]
            }
        """
        await self._ensure_token()

        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"

        # TR ID: FHKST03010200
        headers = self._get_headers("FHKST03010200")

        # Validate interval
        valid_intervals = ["1", "3", "5", "10", "30", "60"]
        if interval not in valid_intervals:
            raise ValueError(f"Invalid interval. Must be one of {valid_intervals}")

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # 시장 분류 코드
            "FID_INPUT_ISCD": symbol,  # 종목코드
            "FID_INPUT_HOUR_1": "",  # 조회 시작시간 (공백: 현재 시간부터)
            "FID_PW_DATA_INCU_YN": "Y",  # 과거 데이터 포함 여부
            "FID_ETC_CLS_CODE": "",  # 기타 구분 코드
        }

        logger.info(f"[KIS API] Calling minute chart data API")
        logger.info(f"  - URL: {url}")
        logger.info(f"  - Symbol: {symbol}")
        logger.info(f"  - Interval: {interval} minutes")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers, params=params)

            logger.info(f"[KIS API] Minute Chart Data Response Status: {response.status_code}")

            if response.status_code != 200:
                logger.error(f"[KIS API] Minute Chart Data Error:")
                logger.error(f"  - Status: {response.status_code}")
                logger.error(f"  - Body: {response.text}")

            response.raise_for_status()
            result = response.json()

            # Log response structure
            if 'rt_cd' in result:
                logger.info(f"  - rt_cd: {result['rt_cd']}")
            if 'msg1' in result:
                logger.info(f"  - msg1: {result['msg1']}")
            if 'output2' in result:
                logger.info(f"  - output2 length: {len(result['output2'])}")

            return result

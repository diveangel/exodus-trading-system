"""KIS API - Market Data & Quotation Services."""

import logging
from typing import Dict, Any

from app.services.kis_client import KISClient

logger = logging.getLogger(__name__)


class KISQuotation:
    """
    KIS API client for market data and quotation services.

    This class provides methods for:
    - Current price queries
    - Historical price data (daily charts)
    - Intraday price data (minute charts)
    """

    def __init__(self, client: KISClient):
        """
        Initialize KIS Quotation service.

        Args:
            client: Authenticated KIS base client
        """
        self.client = client

    async def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price for a stock.

        Args:
            symbol: Stock symbol (e.g., "005930" for Samsung Electronics)

        Returns:
            Dictionary containing current price information
        """
        await self.client._ensure_token()

        url = f"{self.client.base_url}/uapi/domestic-stock/v1/quotations/inquire-price"
        headers = self.client._get_headers("FHKST01010100")
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        }

        return await self.client.get(url, headers, params)

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
        await self.client._ensure_token()

        url = f"{self.client.base_url}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        headers = self.client._get_headers("FHKST03010100")

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # 시장 분류 코드 (J: 주식)
            "FID_INPUT_ISCD": symbol,  # 종목코드
            "FID_INPUT_DATE_1": "",  # 조회 시작일자 (공백: 당일부터 100개)
            "FID_INPUT_DATE_2": "",  # 조회 종료일자
            "FID_PERIOD_DIV_CODE": period,  # 기간분류코드 (D/W/M)
            "FID_ORG_ADJ_PRC": "0" if adjusted_price else "1",  # 수정주가 원주가 가격
        }

        logger.info(f"[KIS Quotation] Calling daily chart data API")
        logger.info(f"  - URL: {url}")
        logger.info(f"  - Symbol: {symbol}")
        logger.info(f"  - Period: {period}")

        result = await self.client.get(url, headers, params)

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
        await self.client._ensure_token()

        url = f"{self.client.base_url}/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"
        headers = self.client._get_headers("FHKST03010200")

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

        logger.info(f"[KIS Quotation] Calling minute chart data API")
        logger.info(f"  - URL: {url}")
        logger.info(f"  - Symbol: {symbol}")
        logger.info(f"  - Interval: {interval} minutes")

        result = await self.client.get(url, headers, params)

        # Log response structure
        if 'rt_cd' in result:
            logger.info(f"  - rt_cd: {result['rt_cd']}")
        if 'msg1' in result:
            logger.info(f"  - msg1: {result['msg1']}")
        if 'output2' in result:
            logger.info(f"  - output2 length: {len(result['output2'])}")

        return result

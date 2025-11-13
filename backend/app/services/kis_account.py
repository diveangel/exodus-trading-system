"""KIS API - Account & Balance Services."""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

from app.services.kis_client import KISClient

logger = logging.getLogger(__name__)


class KISAccount:
    """
    KIS API client for account and balance services.

    This class provides methods for:
    - Account balance queries
    - Holdings information
    - Order history queries
    """

    def __init__(self, client: KISClient):
        """
        Initialize KIS Account service.

        Args:
            client: Authenticated KIS base client
        """
        self.client = client

    async def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance and holdings.

        Returns:
            Dictionary containing account balance information
        """
        await self.client._ensure_token()

        # 국내주식 잔고조회 API
        url = f"{self.client.base_url}/uapi/domestic-stock/v1/trading/inquire-balance"

        # TR ID: VTTC8434R (모의투자), TTTC8434R (실전투자)
        tr_id = "VTTC8434R" if self.client.trading_mode == "MOCK" else "TTTC8434R"
        headers = self.client._get_headers(tr_id)

        params = {
            "CANO": self.client.account_number,
            "ACNT_PRDT_CD": self.client.account_code,
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

        logger.info(f"[KIS Account] Calling account balance API")
        logger.info(f"  - URL: {url}")
        logger.info(f"  - TR ID: {tr_id}")

        result = await self.client.get(url, headers, params)

        # Log response structure for debugging
        logger.info(f"[KIS Account] Response structure:")
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
            logger.info(f"  - output1 type: {type(result['output1'])}")
            if isinstance(result['output1'], dict):
                logger.info(f"  - output1 keys: {list(result['output1'].keys())}")
            logger.info(f"  - output1 value: {result['output1']}")

        if 'output2' in result:
            logger.info(f"  - output2 type: {type(result['output2'])}, length: {len(result['output2']) if isinstance(result['output2'], list) else 'not a list'}")
            if isinstance(result['output2'], list) and len(result['output2']) > 0:
                logger.info(f"  - output2[0] sample: {result['output2'][0]}")

        return result

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
        await self.client._ensure_token()

        if not end_date:
            end_date = datetime.now().strftime("%Y%m%d")
        if not start_date:
            start_date = end_date

        url = f"{self.client.base_url}/uapi/domestic-stock/v1/trading/inquire-daily-ccld"
        headers = self.client._get_headers("TTTC8001R")
        params = {
            "CANO": self.client.account_number,
            "ACNT_PRDT_CD": self.client.account_code,
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

        logger.info(f"[KIS Account] Calling order history API")
        logger.info(f"  - Start Date: {start_date}")
        logger.info(f"  - End Date: {end_date}")

        return await self.client.get(url, headers, params)

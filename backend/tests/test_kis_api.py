"""Tests for Korea Investment & Securities API integration."""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime

from app.services.kis_client import KISClient, KISAuthToken
from app.models.user import User


class TestKISClient:
    """Test KIS API client."""

    @pytest.fixture
    def mock_user(self) -> User:
        """Create a mock user with KIS credentials."""
        user = Mock(spec=User)
        user.kis_app_key = "test_app_key"
        user.kis_app_secret = "test_app_secret"
        user.kis_account_number = "50156093"
        user.kis_account_code = "01"
        user.has_kis_credentials = True
        return user

    @pytest.fixture
    def kis_client(self, mock_user: User) -> KISClient:
        """Create KIS client instance."""
        return KISClient(
            app_key=mock_user.kis_app_key,
            app_secret=mock_user.kis_app_secret,
            account_number=mock_user.kis_account_number,
            account_code=mock_user.kis_account_code,
        )

    @pytest.mark.asyncio
    async def test_get_access_token(self, kis_client: KISClient):
        """Test getting access token from KIS API."""
        # Mock the HTTP response
        mock_response = {
            "access_token": "test_access_token_123",
            "token_type": "Bearer",
            "expires_in": 86400,
        }

        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value = AsyncMock(
                status_code=200,
                json=Mock(return_value=mock_response)
            )

            token = await kis_client.get_access_token()

            assert isinstance(token, KISAuthToken)
            assert token.access_token == "test_access_token_123"
            assert token.token_type == "Bearer"
            assert token.expires_in == 86400

    @pytest.mark.asyncio
    async def test_get_account_balance(self, kis_client: KISClient):
        """Test getting account balance from KIS API."""
        # Mock access token
        kis_client._access_token = KISAuthToken(
            access_token="test_token",
            token_type="Bearer",
            expires_in=86400
        )

        # Mock the HTTP response
        mock_response = {
            "output1": {
                "dnca_tot_amt": "10000000",  # 예수금총액
                "nxdy_excc_amt": "500000",   # 익일정산금액
                "prvs_rcdl_excc_amt": "9500000",  # 가용금액
                "tot_evlu_amt": "15000000",  # 총평가금액
                "pchs_amt_smtl_amt": "14000000",  # 매입금액합계
                "evlu_amt_smtl_amt": "15000000",  # 평가금액합계
                "evlu_pfls_smtl_amt": "1000000",  # 평가손익합계
            },
            "output2": [
                {
                    "pdno": "005930",  # 종목코드
                    "prdt_name": "삼성전자",  # 종목명
                    "hldg_qty": "100",  # 보유수량
                    "pchs_avg_pric": "70000",  # 매입평균가격
                    "pchs_amt": "7000000",  # 매입금액
                    "prpr": "71000",  # 현재가
                    "evlu_amt": "7100000",  # 평가금액
                    "evlu_pfls_amt": "100000",  # 평가손익금액
                    "evlu_pfls_rt": "1.43",  # 평가손익율
                }
            ]
        }

        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.return_value = AsyncMock(
                status_code=200,
                json=Mock(return_value=mock_response)
            )

            balance = await kis_client.get_account_balance()

            assert balance is not None
            assert "output1" in balance
            assert balance["output1"]["tot_evlu_amt"] == "15000000"
            assert len(balance["output2"]) == 1
            assert balance["output2"][0]["pdno"] == "005930"

    @pytest.mark.asyncio
    async def test_get_current_price(self, kis_client: KISClient):
        """Test getting current stock price from KIS API."""
        kis_client._access_token = KISAuthToken(
            access_token="test_token",
            token_type="Bearer",
            expires_in=86400
        )

        # Mock the HTTP response
        mock_response = {
            "output": {
                "stck_prpr": "71000",  # 주식 현재가
                "prdy_vrss": "1000",   # 전일 대비
                "prdy_vrss_sign": "2", # 전일 대비 부호 (2: 상승)
                "prdy_ctrt": "1.43",   # 전일 대비율
                "stck_oprc": "70500",  # 시가
                "stck_hgpr": "71500",  # 고가
                "stck_lwpr": "70000",  # 저가
                "acml_vol": "15000000",  # 누적거래량
            }
        }

        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.return_value = AsyncMock(
                status_code=200,
                json=Mock(return_value=mock_response)
            )

            price = await kis_client.get_current_price("005930")

            assert price is not None
            assert price["output"]["stck_prpr"] == "71000"
            assert price["output"]["prdy_vrss_sign"] == "2"

    @pytest.mark.asyncio
    async def test_place_order_buy(self, kis_client: KISClient):
        """Test placing a buy order through KIS API."""
        kis_client._access_token = KISAuthToken(
            access_token="test_token",
            token_type="Bearer",
            expires_in=86400
        )

        # Mock the HTTP response
        mock_response = {
            "rt_cd": "0",  # 성공 코드
            "msg_cd": "MCA00000",
            "msg1": "주문이 정상적으로 처리되었습니다.",
            "output": {
                "KRX_FWDG_ORD_ORGNO": "91252",
                "ODNO": "0000117057",  # 주문번호
                "ORD_TMD": "121052",   # 주문시각
            }
        }

        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value = AsyncMock(
                status_code=200,
                json=Mock(return_value=mock_response)
            )

            order = await kis_client.place_order(
                symbol="005930",
                order_type="buy",
                quantity=10,
                price=71000
            )

            assert order is not None
            assert order["rt_cd"] == "0"
            assert "ODNO" in order["output"]

    @pytest.mark.asyncio
    async def test_place_order_sell(self, kis_client: KISClient):
        """Test placing a sell order through KIS API."""
        kis_client._access_token = KISAuthToken(
            access_token="test_token",
            token_type="Bearer",
            expires_in=86400
        )

        # Mock the HTTP response
        mock_response = {
            "rt_cd": "0",
            "msg_cd": "MCA00000",
            "msg1": "주문이 정상적으로 처리되었습니다.",
            "output": {
                "KRX_FWDG_ORD_ORGNO": "91252",
                "ODNO": "0000117058",
                "ORD_TMD": "121053",
            }
        }

        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value = AsyncMock(
                status_code=200,
                json=Mock(return_value=mock_response)
            )

            order = await kis_client.place_order(
                symbol="005930",
                order_type="sell",
                quantity=10,
                price=72000
            )

            assert order is not None
            assert order["rt_cd"] == "0"

    @pytest.mark.asyncio
    async def test_get_order_history(self, kis_client: KISClient):
        """Test getting order history from KIS API."""
        kis_client._access_token = KISAuthToken(
            access_token="test_token",
            token_type="Bearer",
            expires_in=86400
        )

        # Mock the HTTP response
        mock_response = {
            "output": [
                {
                    "ord_dt": "20241102",  # 주문일자
                    "ord_gno_brno": "91252",
                    "odno": "0000117057",  # 주문번호
                    "pdno": "005930",  # 종목코드
                    "prdt_name": "삼성전자",  # 종목명
                    "sll_buy_dvsn_cd": "02",  # 매도매수구분 (02: 매수)
                    "ord_qty": "10",  # 주문수량
                    "ord_unpr": "71000",  # 주문단가
                    "ord_tmd": "121052",  # 주문시각
                    "tot_ccld_qty": "10",  # 총체결수량
                    "tot_ccld_amt": "710000",  # 총체결금액
                }
            ]
        }

        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.return_value = AsyncMock(
                status_code=200,
                json=Mock(return_value=mock_response)
            )

            history = await kis_client.get_order_history()

            assert history is not None
            assert len(history["output"]) == 1
            assert history["output"][0]["pdno"] == "005930"
            assert history["output"][0]["sll_buy_dvsn_cd"] == "02"

    @pytest.mark.asyncio
    async def test_token_expiration_and_refresh(self, kis_client: KISClient):
        """Test that expired token is automatically refreshed."""
        # Create an expired token
        expired_token = KISAuthToken(
            access_token="old_token",
            token_type="Bearer",
            expires_in=-1  # Already expired
        )
        kis_client._access_token = expired_token

        # Mock token refresh response
        mock_token_response = {
            "access_token": "new_token_123",
            "token_type": "Bearer",
            "expires_in": 86400,
        }

        # Mock account balance response
        mock_balance_response = {
            "output1": {"tot_evlu_amt": "10000000"},
            "output2": []
        }

        with patch("httpx.AsyncClient.post") as mock_post, \
             patch("httpx.AsyncClient.get") as mock_get:

            mock_post.return_value = AsyncMock(
                status_code=200,
                json=Mock(return_value=mock_token_response)
            )
            mock_get.return_value = AsyncMock(
                status_code=200,
                json=Mock(return_value=mock_balance_response)
            )

            # This should trigger token refresh
            balance = await kis_client.get_account_balance()

            # Verify token was refreshed
            assert kis_client._access_token.access_token == "new_token_123"
            assert balance is not None

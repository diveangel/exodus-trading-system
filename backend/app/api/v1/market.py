"""Market data API endpoints."""

import logging
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.market_data import TimeInterval
from app.schemas.market_data import (
    MarketDataListResponse,
    MarketDataResponse,
    ChartDataResponse,
    ChartDataPoint,
    PriceResponse
)
from app.services.kis_client import KISClient
from app.services.market_data_service import MarketDataService

router = APIRouter()
logger = logging.getLogger(__name__)


def get_kis_client(current_user: User = Depends(get_current_user)) -> KISClient:
    """
    Get KIS client for current user.

    Args:
        current_user: Current authenticated user

    Returns:
        KISClient instance

    Raises:
        HTTPException: If user doesn't have KIS credentials
    """
    if not current_user.has_kis_credentials:
        raise HTTPException(
            status_code=400,
            detail="KIS credentials not configured. Please set up your KIS API credentials in settings."
        )

    return KISClient(
        app_key=current_user.kis_app_key,
        app_secret=current_user.kis_app_secret,
        account_number=current_user.kis_account_number,
        account_code=current_user.kis_account_code,
        trading_mode=current_user.kis_trading_mode.value
    )


@router.post("/collect/daily/{symbol}", response_model=MarketDataListResponse)
async def collect_daily_market_data(
    symbol: str,
    period: str = Query("D", description="Period: D(일), W(주), M(월)"),
    db: AsyncSession = Depends(get_db),
    kis_client: KISClient = Depends(get_kis_client),
    current_user: User = Depends(get_current_user)
):
    """
    Collect daily market data for a symbol from KIS API and save to database.

    Args:
        symbol: Stock symbol (e.g., "005930" for Samsung Electronics)
        period: Period code (D, W, M)
        db: Database session
        kis_client: KIS API client
        current_user: Current user

    Returns:
        MarketDataListResponse with collected data
    """
    try:
        logger.info(f"[Market API] Collecting daily data for {symbol}, period: {period}")

        # Collect data from KIS API
        market_data_list = await MarketDataService.collect_daily_data(
            db=db,
            kis_client=kis_client,
            symbol=symbol,
            period=period
        )

        if not market_data_list:
            raise HTTPException(
                status_code=404,
                detail=f"No market data found for symbol {symbol}"
            )

        # Convert to response format
        data_responses = [MarketDataResponse.model_validate(data) for data in market_data_list]

        return MarketDataListResponse(
            data=data_responses,
            symbol=symbol,
            interval=TimeInterval.ONE_DAY,
            start_date=market_data_list[0].timestamp if market_data_list else datetime.now(),
            end_date=market_data_list[-1].timestamp if market_data_list else datetime.now(),
            total=len(data_responses)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Market API] Error collecting daily data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to collect market data: {str(e)}"
        )


@router.post("/collect/minute/{symbol}", response_model=MarketDataListResponse)
async def collect_minute_market_data(
    symbol: str,
    interval: TimeInterval = Query(
        TimeInterval.THIRTY_MINUTES,
        description="Time interval for minute data"
    ),
    db: AsyncSession = Depends(get_db),
    kis_client: KISClient = Depends(get_kis_client),
    current_user: User = Depends(get_current_user)
):
    """
    Collect minute market data for a symbol from KIS API and save to database.

    Args:
        symbol: Stock symbol
        interval: Time interval (1m, 5m, 10m, 30m, 1h)
        db: Database session
        kis_client: KIS API client
        current_user: Current user

    Returns:
        MarketDataListResponse with collected data
    """
    # Validate interval for minute data
    valid_intervals = [
        TimeInterval.ONE_MINUTE,
        TimeInterval.FIVE_MINUTES,
        TimeInterval.TEN_MINUTES,
        TimeInterval.THIRTY_MINUTES,
        TimeInterval.ONE_HOUR
    ]

    if interval not in valid_intervals:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid interval for minute data. Must be one of: {[i.value for i in valid_intervals]}"
        )

    try:
        logger.info(f"[Market API] Collecting {interval} data for {symbol}")

        # Collect data from KIS API
        market_data_list = await MarketDataService.collect_minute_data(
            db=db,
            kis_client=kis_client,
            symbol=symbol,
            interval=interval
        )

        if not market_data_list:
            raise HTTPException(
                status_code=404,
                detail=f"No market data found for symbol {symbol}"
            )

        # Convert to response format
        data_responses = [MarketDataResponse.model_validate(data) for data in market_data_list]

        return MarketDataListResponse(
            data=data_responses,
            symbol=symbol,
            interval=interval,
            start_date=market_data_list[0].timestamp if market_data_list else datetime.now(),
            end_date=market_data_list[-1].timestamp if market_data_list else datetime.now(),
            total=len(data_responses)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Market API] Error collecting minute data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to collect market data: {str(e)}"
        )


@router.get("/chart/{symbol}", response_model=ChartDataResponse)
async def get_chart_data(
    symbol: str,
    interval: TimeInterval = Query(TimeInterval.ONE_DAY, description="Time interval"),
    days: int = Query(30, ge=1, le=365, description="Number of days to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get chart data for a symbol from database.

    Args:
        symbol: Stock symbol
        interval: Time interval
        days: Number of days to retrieve
        db: Database session
        current_user: Current user

    Returns:
        ChartDataResponse with chart data points
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Get data from database
        market_data_list = await MarketDataService.get_market_data(
            db=db,
            symbol=symbol,
            interval=interval,
            start_date=start_date,
            end_date=end_date,
            limit=1000
        )

        if not market_data_list:
            raise HTTPException(
                status_code=404,
                detail=f"No chart data found for symbol {symbol}. Try collecting data first."
            )

        # Convert to chart data points
        chart_points = [
            ChartDataPoint(
                timestamp=data.timestamp,
                open=data.open,
                high=data.high,
                low=data.low,
                close=data.close,
                volume=data.volume
            )
            for data in market_data_list
        ]

        return ChartDataResponse(
            symbol=symbol,
            interval=interval,
            data=chart_points
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Market API] Error getting chart data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get chart data: {str(e)}"
        )


@router.get("/price/{symbol}", response_model=PriceResponse)
async def get_current_price(
    symbol: str,
    db: AsyncSession = Depends(get_db),
    kis_client: KISClient = Depends(get_kis_client),
    current_user: User = Depends(get_current_user)
):
    """
    Get current price for a symbol from KIS API.

    Args:
        symbol: Stock symbol
        db: Database session
        kis_client: KIS API client
        current_user: Current user

    Returns:
        PriceResponse with current price information
    """
    try:
        logger.info(f"[Market API] Getting current price for {symbol}")

        # Get current price from KIS API
        kis_response = await kis_client.get_current_price(symbol)

        if 'output' not in kis_response:
            raise HTTPException(
                status_code=404,
                detail=f"No price data found for symbol {symbol}"
            )

        output = kis_response['output']

        # Parse response
        current_price = float(output.get('stck_prpr', 0))  # 현재가
        change = float(output.get('prdy_vrss', 0))  # 전일대비
        change_percent = float(output.get('prdy_ctrt', 0))  # 전일대비율
        volume = float(output.get('acml_vol', 0))  # 누적거래량

        # Get timestamp from KIS API response
        # stck_bsop_date: 영업일자 (YYYYMMDD)
        # stck_cntg_hour: 체결시간 (HHMMSS)
        trade_date = output.get('stck_bsop_date', '')  # 영업일자
        trade_time = output.get('stck_cntg_hour', '')  # 체결시간

        # Parse datetime from KIS API response
        if trade_date and trade_time:
            # Format: YYYYMMDD + HHMMSS
            datetime_str = f"{trade_date}{trade_time}"
            try:
                kis_timestamp = datetime.strptime(datetime_str, "%Y%m%d%H%M%S")
            except ValueError:
                logger.warning(f"Failed to parse KIS timestamp: {datetime_str}")
                kis_timestamp = datetime.now()
        else:
            logger.warning("KIS API response missing date/time fields")
            kis_timestamp = datetime.now()

        return PriceResponse(
            symbol=symbol,
            price=current_price,
            change=change,
            change_percent=change_percent,
            volume=volume,
            timestamp=kis_timestamp
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Market API] Error getting current price: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get current price: {str(e)}"
        )


@router.get("/latest/{symbol}", response_model=MarketDataResponse)
async def get_latest_market_data(
    symbol: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the latest market data for a symbol from database.

    Args:
        symbol: Stock symbol
        db: Database session
        current_user: Current user

    Returns:
        MarketDataResponse with latest data
    """
    try:
        latest_data = await MarketDataService.get_latest_price(db=db, symbol=symbol)

        if not latest_data:
            raise HTTPException(
                status_code=404,
                detail=f"No market data found for symbol {symbol}"
            )

        return MarketDataResponse.model_validate(latest_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Market API] Error getting latest data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get latest data: {str(e)}"
        )

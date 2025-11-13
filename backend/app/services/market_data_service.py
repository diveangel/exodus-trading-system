"""Market data service for collecting and managing market data."""

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.market_data import MarketData, TimeInterval
from app.schemas.market_data import MarketDataCreate
from app.services.kis_quotation import KISQuotation

logger = logging.getLogger(__name__)


class MarketDataService:
    """Service for managing market data operations."""

    @staticmethod
    def _parse_daily_chart_data(
        symbol: str,
        kis_response: Dict[str, Any],
        interval: TimeInterval = TimeInterval.ONE_DAY
    ) -> List[MarketDataCreate]:
        """
        Parse KIS daily chart API response to MarketData objects.

        Args:
            symbol: Stock symbol
            kis_response: Response from KIS API
            interval: Time interval (default: ONE_DAY)

        Returns:
            List of MarketDataCreate objects
        """
        market_data_list = []

        if 'output2' not in kis_response or not kis_response['output2']:
            logger.warning(f"No chart data found for symbol {symbol}")
            return market_data_list

        for item in kis_response['output2']:
            try:
                # Parse date: YYYYMMDD format
                date_str = item['stck_bsop_date']
                timestamp = datetime.strptime(date_str, "%Y%m%d")

                market_data = MarketDataCreate(
                    symbol=symbol,
                    timestamp=timestamp,
                    open=float(item['stck_oprc']),
                    high=float(item['stck_hgpr']),
                    low=float(item['stck_lwpr']),
                    close=float(item['stck_clpr']),
                    volume=float(item['acml_vol']),
                    interval=interval
                )
                market_data_list.append(market_data)
            except (KeyError, ValueError) as e:
                logger.error(f"Error parsing chart data item: {e}, item: {item}")
                continue

        logger.info(f"Parsed {len(market_data_list)} chart data records for {symbol}")
        return market_data_list

    @staticmethod
    def _parse_minute_chart_data(
        symbol: str,
        kis_response: Dict[str, Any],
        interval: TimeInterval
    ) -> List[MarketDataCreate]:
        """
        Parse KIS minute chart API response to MarketData objects.

        Args:
            symbol: Stock symbol
            kis_response: Response from KIS API
            interval: Time interval (e.g., ONE_MINUTE, FIVE_MINUTES)

        Returns:
            List of MarketDataCreate objects
        """
        market_data_list = []

        if 'output2' not in kis_response or not kis_response['output2']:
            logger.warning(f"No minute chart data found for symbol {symbol}")
            return market_data_list

        for item in kis_response['output2']:
            try:
                # Parse datetime: YYYYMMDD + HHMMSS
                date_str = item['stck_bsop_date']
                time_str = item['stck_cntg_hour']
                timestamp = datetime.strptime(f"{date_str}{time_str}", "%Y%m%d%H%M%S")

                market_data = MarketDataCreate(
                    symbol=symbol,
                    timestamp=timestamp,
                    open=float(item['stck_oprc']),
                    high=float(item['stck_hgpr']),
                    low=float(item['stck_lwpr']),
                    close=float(item['stck_prpr']),  # 현재가 (종가 대신)
                    volume=float(item['cntg_vol']),
                    interval=interval
                )
                market_data_list.append(market_data)
            except (KeyError, ValueError) as e:
                logger.error(f"Error parsing minute chart data item: {e}, item: {item}")
                continue

        logger.info(f"Parsed {len(market_data_list)} minute chart data records for {symbol}")
        return market_data_list

    @staticmethod
    async def collect_daily_data(
        db: AsyncSession,
        kis_client: KISQuotation,
        symbol: str,
        period: str = "D"
    ) -> List[MarketData]:
        """
        Collect daily chart data from KIS API and save to database.

        Args:
            db: Database session
            kis_client: KIS API client
            symbol: Stock symbol
            period: Period code (D: 일, W: 주, M: 월)

        Returns:
            List of saved MarketData objects
        """
        logger.info(f"Collecting daily data for {symbol}, period: {period}")

        # Get data from KIS API
        kis_response = await kis_client.get_daily_chart_data(symbol, period)

        # Parse response
        market_data_list = MarketDataService._parse_daily_chart_data(
            symbol=symbol,
            kis_response=kis_response,
            interval=TimeInterval.ONE_DAY
        )

        # Save to database
        saved_data = []
        for data in market_data_list:
            # Check if data already exists
            stmt = select(MarketData).where(
                and_(
                    MarketData.symbol == data.symbol,
                    MarketData.timestamp == data.timestamp,
                    MarketData.interval == data.interval
                )
            )
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                # Update existing data
                existing.open = data.open
                existing.high = data.high
                existing.low = data.low
                existing.close = data.close
                existing.volume = data.volume
                saved_data.append(existing)
            else:
                # Create new data
                new_data = MarketData(**data.model_dump())
                db.add(new_data)
                saved_data.append(new_data)

        await db.commit()
        logger.info(f"Saved {len(saved_data)} daily data records for {symbol}")

        return saved_data

    @staticmethod
    async def collect_minute_data(
        db: AsyncSession,
        kis_client: KISQuotation,
        symbol: str,
        interval: TimeInterval
    ) -> List[MarketData]:
        """
        Collect minute chart data from KIS API and save to database.

        Args:
            db: Database session
            kis_client: KIS API client
            symbol: Stock symbol
            interval: Time interval (ONE_MINUTE, FIVE_MINUTES, etc.)

        Returns:
            List of saved MarketData objects
        """
        # Map TimeInterval to KIS API interval parameter
        interval_map = {
            TimeInterval.ONE_MINUTE: "1",
            TimeInterval.FIVE_MINUTES: "5",
            TimeInterval.TEN_MINUTES: "10",
            TimeInterval.THIRTY_MINUTES: "30",
            TimeInterval.ONE_HOUR: "60",
        }

        if interval not in interval_map:
            raise ValueError(f"Unsupported interval: {interval}")

        kis_interval = interval_map[interval]
        logger.info(f"Collecting {interval} data for {symbol}")

        # Get data from KIS API
        kis_response = await kis_client.get_minute_chart_data(symbol, kis_interval)

        # Parse response
        market_data_list = MarketDataService._parse_minute_chart_data(
            symbol=symbol,
            kis_response=kis_response,
            interval=interval
        )

        # Save to database
        saved_data = []
        for data in market_data_list:
            # Check if data already exists
            stmt = select(MarketData).where(
                and_(
                    MarketData.symbol == data.symbol,
                    MarketData.timestamp == data.timestamp,
                    MarketData.interval == data.interval
                )
            )
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                # Update existing data
                existing.open = data.open
                existing.high = data.high
                existing.low = data.low
                existing.close = data.close
                existing.volume = data.volume
                saved_data.append(existing)
            else:
                # Create new data
                new_data = MarketData(**data.model_dump())
                db.add(new_data)
                saved_data.append(new_data)

        await db.commit()
        logger.info(f"Saved {len(saved_data)} {interval} data records for {symbol}")

        return saved_data

    @staticmethod
    async def get_market_data(
        db: AsyncSession,
        symbol: str,
        interval: TimeInterval,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[MarketData]:
        """
        Get market data from database.

        Args:
            db: Database session
            symbol: Stock symbol
            interval: Time interval
            start_date: Start date (optional)
            end_date: End date (optional)
            limit: Maximum number of records to return

        Returns:
            List of MarketData objects
        """
        # Build query
        conditions = [
            MarketData.symbol == symbol,
            MarketData.interval == interval
        ]

        if start_date:
            conditions.append(MarketData.timestamp >= start_date)
        if end_date:
            conditions.append(MarketData.timestamp <= end_date)

        stmt = (
            select(MarketData)
            .where(and_(*conditions))
            .order_by(MarketData.timestamp.desc())
            .limit(limit)
        )

        result = await db.execute(stmt)
        data = result.scalars().all()

        # Return in chronological order
        return list(reversed(data))

    @staticmethod
    async def get_latest_price(
        db: AsyncSession,
        symbol: str
    ) -> Optional[MarketData]:
        """
        Get the latest price data for a symbol.

        Args:
            db: Database session
            symbol: Stock symbol

        Returns:
            Latest MarketData object or None
        """
        stmt = (
            select(MarketData)
            .where(MarketData.symbol == symbol)
            .order_by(MarketData.timestamp.desc())
            .limit(1)
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none()

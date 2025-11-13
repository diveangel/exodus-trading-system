"""Stock model for storing KOSPI/KOSDAQ stock information."""

from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Date, Index
from sqlalchemy.sql import func

from app.db.base import Base


class Stock(Base):
    """Stock information from KOSPI/KOSDAQ master files."""

    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, nullable=False, index=True)
    standard_code = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False, index=True)
    market_type = Column(String(10), nullable=False, index=True)  # KOSPI or KOSDAQ

    # Additional stock information
    dept = Column(String(50), nullable=True, index=True)  # KRX department (부문)
    sector = Column(String(50), nullable=True, index=True)  # Sector classification
    industry = Column(String(100), nullable=True, index=True)  # Industry classification
    market_cap = Column(BigInteger, nullable=True, index=True)  # Market capitalization
    listing_date = Column(Date, nullable=True)  # Listing date

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Create composite index for searching
    __table_args__ = (
        Index('ix_stocks_name_symbol', 'name', 'symbol'),
        Index('ix_stocks_market_name', 'market_type', 'name'),
    )

    def __repr__(self):
        return f"<Stock {self.symbol} - {self.name}>"

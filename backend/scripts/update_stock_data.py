"""
Update stock data from FinanceDataReader
- Updates dept (부문) and market_cap for all stocks
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import asyncio
import FinanceDataReader as fdr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.stock import Stock
from app.config import settings

async def update_stock_data():
    """Update stock data from FinanceDataReader"""
    
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    print("Fetching KRX stock list from FinanceDataReader...")
    krx_stocks = fdr.StockListing('KRX')
    
    print(f"Total stocks fetched: {len(krx_stocks)}")
    print(f"Columns: {list(krx_stocks.columns)}")
    
    # Code, Name, Market, Dept, Marcap 컬럼 사용
    updated_count = 0
    not_found_count = 0
    
    async with async_session() as session:
        for idx, row in krx_stocks.iterrows():
            code = row['Code']
            name = row['Name']
            dept = row['Dept'] if row['Dept'] else None
            marcap = int(row['Marcap']) if row['Marcap'] and row['Marcap'] > 0 else None
            
            # Find stock by symbol
            stmt = select(Stock).where(Stock.symbol == code)
            result = await session.execute(stmt)
            stock = result.scalar_one_or_none()
            
            if stock:
                # Update dept and market_cap
                stock.dept = dept
                stock.market_cap = marcap
                updated_count += 1
                
                if updated_count % 100 == 0:
                    print(f"Updated {updated_count} stocks...")
                    await session.commit()
            else:
                not_found_count += 1
                if not_found_count <= 10:  # Show first 10
                    print(f"Stock not found in DB: {code} - {name}")
        
        # Final commit
        await session.commit()
    
    print(f"\n=== Update Complete ===")
    print(f"Total stocks in FDR: {len(krx_stocks)}")
    print(f"Updated: {updated_count}")
    print(f"Not found in DB: {not_found_count}")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(update_stock_data())

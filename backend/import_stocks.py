"""Import KOSPI/KOSDAQ stock data into database."""

import asyncio
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.db.session import AsyncSessionLocal
from app.models.stock import Stock


def parse_stock_code(data: bytes, market_type: str) -> dict | None:
    """Parse stock code data from master file.

    Args:
        data: Binary data record
        market_type: 'KOSPI' or 'KOSDAQ'

    Returns:
        Dictionary with stock info or None if parsing failed
    """
    try:
        return {
            'symbol': data[0:9].decode('cp949').strip(),
            'standard_code': data[9:21].decode('cp949').strip(),
            'name': data[21:61].decode('cp949').strip(),
            'market_type': market_type
        }
    except Exception as e:
        # Skip records that can't be decoded
        return None


def read_stock_master(file_path: Path, market_type: str) -> list[dict]:
    """Read stock master file and parse all records.

    Args:
        file_path: Path to master file (.mst)
        market_type: 'KOSPI' or 'KOSDAQ'

    Returns:
        List of stock dictionaries
    """
    stocks = []

    with open(file_path, 'rb') as f:
        data = f.read()
        records = data.split(b'\n')

        for record in records:
            if len(record) < 60:
                continue

            stock = parse_stock_code(record, market_type)
            if stock and stock['symbol']:
                stocks.append(stock)

    return stocks


async def import_stocks():
    """Import all stock data from KOSPI and KOSDAQ master files."""
    data_dir = Path(__file__).parent.parent / 'data'

    print("Reading KOSPI master file...")
    kospi_stocks = read_stock_master(data_dir / 'kospi_code.mst', 'KOSPI')
    print(f"✓ Parsed {len(kospi_stocks)} KOSPI stocks")

    print("\nReading KOSDAQ master file...")
    kosdaq_stocks = read_stock_master(data_dir / 'kosdaq_code.mst', 'KOSDAQ')
    print(f"✓ Parsed {len(kosdaq_stocks)} KOSDAQ stocks")

    all_stocks = kospi_stocks + kosdaq_stocks
    print(f"\nTotal stocks to import: {len(all_stocks)}")

    # Insert into database
    async with AsyncSessionLocal() as session:
        print("\nImporting stocks into database...")

        # Use PostgreSQL's INSERT ON CONFLICT for upsert
        for i, stock_data in enumerate(all_stocks, 1):
            stmt = insert(Stock).values(**stock_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=['symbol'],
                set_={
                    'name': stmt.excluded.name,
                    'standard_code': stmt.excluded.standard_code,
                    'market_type': stmt.excluded.market_type,
                }
            )
            await session.execute(stmt)

            if i % 100 == 0:
                print(f"  Imported {i}/{len(all_stocks)} stocks...")
                await session.commit()

        await session.commit()
        print(f"✓ Successfully imported all {len(all_stocks)} stocks")

    # Verify import
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Stock))
        total = len(result.scalars().all())
        print(f"\n✓ Verification: Database contains {total} stocks")

        # Show some examples
        result = await session.execute(
            select(Stock).filter(Stock.symbol.in_(['005930', '035720', '000660']))
        )
        examples = result.scalars().all()
        print("\nExample stocks:")
        for stock in examples:
            print(f"  {stock.symbol:10} {stock.name:30} {stock.market_type}")


if __name__ == "__main__":
    asyncio.run(import_stocks())

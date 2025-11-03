"""Parse KOSPI/KOSDAQ stock master files."""

import struct
from pathlib import Path


def parse_kospi_code(data: bytes) -> dict:
    """Parse KOSPI stock code data.

    Based on: https://github.com/koreainvestment/open-trading-api/blob/main/stocks_info/
    """
    # The file uses EUC-KR encoding for Korean text
    try:
        return {
            'symbol': data[0:9].decode('cp949').strip(),              # 단축코드
            'standard_code': data[9:21].decode('cp949').strip(),      # 표준코드
            'name': data[21:61].decode('cp949').strip(),              # 한글종목명
            'market_type': 'KOSPI'
        }
    except Exception as e:
        print(f"Error parsing: {e}")
        return None


def parse_kosdaq_code(data: bytes) -> dict:
    """Parse KOSDAQ stock code data.

    Similar structure to KOSPI but with some different fields.
    """
    try:
        return {
            'symbol': data[0:9].decode('cp949').strip(),              # 단축코드
            'standard_code': data[9:21].decode('cp949').strip(),      # 표준코드
            'name': data[21:61].decode('cp949').strip(),              # 한글종목명
            'market_type': 'KOSDAQ'
        }
    except Exception as e:
        print(f"Error parsing: {e}")
        return None


def read_stock_master(file_path: Path, parser_func) -> list:
    """Read stock master file and parse records."""
    stocks = []

    with open(file_path, 'rb') as f:
        # Read the entire file
        data = f.read()

        # Each record is separated by newline (0x0A)
        # Split by newline and process each record
        records = data.split(b'\n')

        for record in records:
            if len(record) < 60:  # Skip short records
                continue

            stock = parser_func(record)
            if stock and stock['symbol']:
                stocks.append(stock)

    return stocks


if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / 'data'

    print("Parsing KOSPI stocks...")
    kospi_stocks = read_stock_master(data_dir / 'kospi_code.mst', parse_kospi_code)
    print(f"Found {len(kospi_stocks)} KOSPI stocks")
    print("Sample:", kospi_stocks[:3])

    print("\nParsing KOSDAQ stocks...")
    kosdaq_stocks = read_stock_master(data_dir / 'kosdaq_code.mst', parse_kosdaq_code)
    print(f"Found {len(kosdaq_stocks)} KOSDAQ stocks")
    print("Sample:", kosdaq_stocks[:3])

    # Print some examples for verification
    print("\n=== KOSPI Examples ===")
    for stock in kospi_stocks[:5]:
        print(f"{stock['symbol']:10} {stock['name']:30} {stock['market_type']}")

    print("\n=== KOSDAQ Examples ===")
    for stock in kosdaq_stocks[:5]:
        print(f"{stock['symbol']:10} {stock['name']:30} {stock['market_type']}")

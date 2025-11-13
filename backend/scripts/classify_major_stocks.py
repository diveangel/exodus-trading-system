"""
Manually classify sector and industry for major stocks
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.stock import Stock
from app.config import settings


# Manual classification for top stocks by market cap
# Format: symbol: (sector, industry)
STOCK_CLASSIFICATIONS = {
    # Top 1-10
    '005930': ('Technology', '반도체'),  # 삼성전자
    '000660': ('Technology', '반도체'),  # SK하이닉스
    '373220': ('Energy', '2차전지'),  # LG에너지솔루션
    '207940': ('Healthcare', '바이오의약품'),  # 삼성바이오로직스
    '005935': ('Technology', '반도체'),  # 삼성전자우
    '005380': ('Automotive', '자동차제조'),  # 현대차
    '034020': ('Energy', '발전설비'),  # 두산에너빌리티
    '012450': ('Aerospace', '항공우주방산'),  # 한화에어로스페이스
    '105560': ('Finance', '금융지주'),  # KB금융
    '329180': ('Industrial', '조선'),  # HD현대중공업

    # Top 11-20
    '000270': ('Automotive', '자동차제조'),  # 기아
    '035420': ('Technology', '인터넷플랫폼'),  # NAVER
    '068270': ('Healthcare', '바이오의약품'),  # 셀트리온
    '042660': ('Industrial', '조선'),  # 한화오션
    '055550': ('Finance', '금융지주'),  # 신한지주
    '402340': ('Technology', 'IT지주'),  # SK스퀘어
    '028260': ('Industrial', '종합상사'),  # 삼성물산
    '032830': ('Finance', '보험'),  # 삼성생명
    '267260': ('Industrial', '전기장비'),  # HD현대일렉트릭
    '009540': ('Industrial', '조선'),  # HD한국조선해양

    # Top 21-30
    '015760': ('Energy', '전력공급'),  # 한국전력
    '196170': ('Healthcare', '바이오의약품'),  # 알테오젠
    '035720': ('Technology', '인터넷플랫폼'),  # 카카오
    '051910': ('Chemicals', '석유화학'),  # LG화학
    '012330': ('Automotive', '자동차부품'),  # 현대모비스
    '086790': ('Finance', '금융지주'),  # 하나금융지주
    '006400': ('Energy', '2차전지'),  # 삼성SDI
    '005490': ('Industrial', '철강'),  # POSCO홀딩스
    '010140': ('Industrial', '조선'),  # 삼성중공업
    '000810': ('Finance', '보험'),  # 삼성화재

    # Top 31-40
    '064350': ('Industrial', '철도차량'),  # 현대로템
    '298040': ('Industrial', '중전기'),  # 효성중공업
    '138040': ('Finance', '금융지주'),  # 메리츠금융지주
    '010130': ('Chemicals', '비철금속'),  # 고려아연
    '096770': ('Energy', '석유정제'),  # SK이노베이션
    '316140': ('Finance', '금융지주'),  # 우리금융지주
    '011200': ('Transport', '해운'),  # HMM
    '003670': ('Chemicals', '2차전지소재'),  # 포스코퓨처엠
    '034730': ('Industrial', '지주회사'),  # SK
    '009150': ('Technology', '전자부품'),  # 삼성전기

    # Top 41-50
    '267250': ('Industrial', '중공업지주'),  # HD현대
    '033780': ('Consumer', '담배/식품'),  # KT&G
    '024110': ('Finance', '은행'),  # 기업은행
    '000150': ('Industrial', '지주회사'),  # 두산
    '247540': ('Energy', '2차전지소재'),  # 에코프로비엠
    '066570': ('Technology', '가전/전자'),  # LG전자
    '010120': ('Industrial', '전기장비'),  # LS ELECTRIC
    '006800': ('Finance', '증권'),  # 미래에셋증권
    '018260': ('Technology', 'IT서비스'),  # 삼성에스디에스
    '352820': ('Entertainment', '엔터테인먼트'),  # 하이브
}


async def classify_stocks():
    """Update sector and industry for major stocks"""

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    print("Classifying major stocks by sector and industry...\n")

    updated_count = 0
    not_found_count = 0

    async with async_session() as session:
        for symbol, (sector, industry) in STOCK_CLASSIFICATIONS.items():
            # Find stock by symbol
            stmt = select(Stock).where(Stock.symbol == symbol)
            result = await session.execute(stmt)
            stock = result.scalar_one_or_none()

            if stock:
                stock.sector = sector
                stock.industry = industry
                updated_count += 1
                print(f"✓ {symbol:>6} - {stock.name:<20} → {sector:<15} / {industry}")
            else:
                not_found_count += 1
                print(f"✗ {symbol:>6} - Not found in database")

        await session.commit()

    print(f"\n{'='*70}")
    print(f"Classification Complete:")
    print(f"  Updated: {updated_count}")
    print(f"  Not found: {not_found_count}")
    print(f"{'='*70}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(classify_stocks())

# Exodus Trading System - Architecture Documentation

**버전:** 1.0
**작성일:** 2025-11-12
**상태:** Sprint 2 완료 시점

---

## 목차

1. [시스템 개요](#시스템-개요)
2. [기술 스택](#기술-스택)
3. [High-Level Architecture](#high-level-architecture)
4. [Backend Architecture](#backend-architecture)
5. [Frontend Architecture](#frontend-architecture)
6. [Database Design](#database-design)
7. [Integration Points](#integration-points)
8. [Security Architecture](#security-architecture)
9. [Deployment Architecture](#deployment-architecture)
10. [API Documentation](#api-documentation)

---

## 시스템 개요

### MVP 목표

Exodus Trading System은 한국투자증권 OpenAPI를 활용한 **자동 매매 시스템 MVP**입니다.

**핵심 기능:**
- 퀀트 투자 전략 생성 및 관리
- 백테스팅을 통한 전략 검증
- 실시간 시장 데이터 모니터링
- 자동/수동 주문 실행
- 계좌 및 포트폴리오 관리

**사용자 타입:**
- 개인 퀀트 투자자
- 알고리즘 트레이더
- 시스템 트레이딩 학습자

---

## 기술 스택

### Backend

| 카테고리 | 기술 | 버전 | 용도 |
|---------|------|------|------|
| **Framework** | FastAPI | 0.115+ | REST API 서버 |
| **Language** | Python | 3.12 | 백엔드 로직 |
| **Database** | PostgreSQL | 15 | 데이터 영속성 |
| **ORM** | SQLAlchemy | 2.0+ | ORM (Async) |
| **Migration** | Alembic | Latest | DB 마이그레이션 |
| **Authentication** | python-jose | Latest | JWT 토큰 |
| **Password** | bcrypt | Latest | 비밀번호 해싱 |
| **HTTP Client** | httpx | Latest | KIS API 호출 (Async) |
| **Validation** | Pydantic | 2.0+ | 데이터 검증 |
| **Testing** | pytest | Latest | 단위/통합 테스트 |

### Frontend

| 카테고리 | 기술 | 버전 | 용도 |
|---------|------|------|------|
| **Framework** | Next.js | 14.2.33 | React Framework |
| **Language** | TypeScript | Latest | 타입 안정성 |
| **UI Library** | React | 18 | UI 컴포넌트 |
| **Styling** | Tailwind CSS | Latest | CSS Framework |
| **Components** | shadcn/ui | Latest | UI 컴포넌트 라이브러리 |
| **HTTP Client** | Axios | Latest | API 통신 |
| **Forms** | React Hook Form | Latest | 폼 관리 |
| **Validation** | Zod | Latest | 스키마 검증 |
| **Charts** | Recharts | Latest | 데이터 시각화 |
| **Icons** | Lucide React | Latest | 아이콘 |

### Infrastructure

| 카테고리 | 기술 | 용도 |
|---------|------|------|
| **Containerization** | Docker | 개발/배포 환경 |
| **Orchestration** | Docker Compose | 로컬 개발 |
| **Version Control** | Git | 소스 관리 |
| **Database** | postgres:15-alpine | PostgreSQL 컨테이너 |

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Client Browser                          │
│                      (React + TypeScript)                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP/REST
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Next.js Frontend (Port 3000)                 │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │  App Router    │  │   Components   │  │   API Clients  │   │
│  │   (Pages)      │  │  (UI Library)  │  │   (Axios)      │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP REST API (JWT Auth)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Port 8000)                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                      API Layer (v1)                         │ │
│  │  Auth│Account│Market│Strategy│Backtest│Stocks│Watchlist   │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Core Business Logic                      │ │
│  │  Strategy Engine │ Backtest Engine │ Indicators           │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     Service Layer                           │ │
│  │  KIS Client │ Account │ Quotation │ Trading │ Data Service │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Data Access Layer                         │ │
│  │  Models │ Repositories │ Alembic Migrations                │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────┬───────────────────────────┬──────────────────────┘
               │                           │ HTTPS
               │ PostgreSQL                │
               ▼                           ▼
┌──────────────────────────┐  ┌─────────────────────────────────┐
│  PostgreSQL Database     │  │  KIS OpenAPI (External)         │
│  (Port 5432)             │  │  - Real Trading Mode            │
│  - Users                 │  │  - Mock Trading Mode            │
│  - Strategies            │  │  - Market Data                  │
│  - Market Data           │  │  - Account Info                 │
│  - Orders/Trades         │  │  - Order Execution              │
│  - Holdings/Signals      │  │                                 │
└──────────────────────────┘  └─────────────────────────────────┘
```

---

## Backend Architecture

### 계층 구조 (Layered Architecture)

```
backend/app/
├── api/v1/              → API Layer (HTTP Endpoints)
├── core/                → Core Business Logic
│   ├── strategy/        → Strategy Engine
│   ├── backtest/        → Backtest Engine (예정)
│   └── indicators/      → Technical Indicators
├── services/            → External Service Integration
│   └── kis_*/           → KIS API Client Services
├── models/              → Data Models (SQLAlchemy ORM)
├── schemas/             → API Schemas (Pydantic)
├── db/                  → Database Session Management
└── core/                → Core Utilities (Security, Config, etc.)
```

### 1. API Layer (`api/v1/`)

**역할:** HTTP 요청 처리 및 응답 반환

**구성 요소:**

| 파일 | 엔드포인트 수 | 주요 기능 |
|------|-------------|----------|
| `auth.py` | 5 | 회원가입, 로그인, 토큰 관리 |
| `account.py` | 6 | 계좌 정보, KIS 인증 관리 |
| `market.py` | 5 | 시장 데이터 수집 및 조회 |
| `strategy.py` | 8 | 전략 CRUD 및 실행 |
| `stocks.py` | 4 | 종목 검색 및 필터링 |
| `watchlist.py` | 5 | 관심종목 관리 |
| `dashboard.py` | 1 | 대시보드 데이터 |
| `backtest.py` | 3 | 백테스트 실행/결과 |

**설계 원칙:**
- ✅ RESTful API 설계
- ✅ Dependency Injection (FastAPI Depends)
- ✅ 포괄적 에러 처리 (HTTPException)
- ✅ OpenAPI 자동 문서화
- ✅ Request/Response Validation (Pydantic)

**예시 구조:**

```python
# api/v1/strategy.py
@router.post("/", response_model=StrategyResponse, status_code=201)
async def create_strategy(
    strategy_data: StrategyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """전략 생성 엔드포인트"""
    # 1. 권한 확인 (Dependency에서 처리)
    # 2. 비즈니스 로직 실행 (Service Layer 호출)
    # 3. DB 저장
    # 4. 응답 반환
    return strategy
```

---

### 2. Core Business Logic (`core/`)

**역할:** 핵심 비즈니스 로직 및 알고리즘 구현

#### 2.1 Strategy Engine (`core/strategy/`)

**구조:**

```
core/strategy/
├── base.py           # Strategy 추상 클래스
├── momentum.py       # Momentum 전략 구현
├── mean_reversion.py # Mean Reversion 전략 (예정)
└── types.py          # Strategy Type 정의
```

**Strategy 추상 클래스:**

```python
class Strategy(ABC):
    """전략 베이스 클래스"""

    @abstractmethod
    async def generate_signals(
        self,
        market_data: List[MarketData],
        context: Dict
    ) -> List[Signal]:
        """신호 생성 로직"""
        pass

    @abstractmethod
    def validate_parameters(self, params: Dict) -> bool:
        """파라미터 검증"""
        pass
```

**Momentum 전략 예시:**

```python
class MomentumStrategy(Strategy):
    """SMA 크로스오버 모멘텀 전략"""

    async def generate_signals(self, market_data, context):
        # 1. 이동평균 계산 (fast_period, slow_period)
        # 2. 크로스오버 감지
        # 3. 매수/매도 신호 생성
        # 4. Signal 객체 반환
        return signals
```

#### 2.2 Backtest Engine (`core/backtest/`) - 예정

**구조:**

```
core/backtest/
├── engine.py        # 백테스트 엔진 코어
├── portfolio.py     # 포트폴리오 시뮬레이터
├── executor.py      # 주문 실행 시뮬레이터
├── metrics.py       # 성과 지표 계산
└── analyzer.py      # 결과 분석
```

**설계 (예정):**

```python
class BacktestEngine:
    async def run(
        self,
        strategy: Strategy,
        start_date: date,
        end_date: date,
        initial_capital: float
    ) -> BacktestResult:
        # 1. 시장 데이터 로드
        # 2. 전략 신호 생성
        # 3. 포트폴리오 시뮬레이션
        # 4. 성과 지표 계산
        # 5. 결과 반환
        pass
```

#### 2.3 Technical Indicators (`core/indicators/`)

**구현 예정:**
- SMA (Simple Moving Average)
- EMA (Exponential Moving Average)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands

---

### 3. Service Layer (`services/`)

**역할:** 외부 시스템 통합 및 데이터 가공

#### 3.1 KIS API Integration

**구조:**

```
services/
├── kis_client.py         # Base Client (토큰 관리)
├── kis_account.py        # 계좌 조회
├── kis_quotation.py      # 시세 조회
├── kis_trading.py        # 주문 실행
├── kis_token_manager.py  # 토큰 영속화
├── market_data_service.py # 시장 데이터 수집
└── strategy_service.py   # 전략 관리 서비스
```

**KIS Client 아키텍처:**

```python
class KISClient:
    """KIS API 기본 클라이언트"""

    def __init__(self, mode: TradingMode):
        self.base_url = self._get_base_url(mode)
        self.token_manager = KISTokenManager()

    async def _ensure_token(self, credentials):
        """토큰 자동 갱신"""
        if not self.token_manager.is_valid():
            await self._refresh_token()

    async def request(self, endpoint, params):
        """공통 요청 처리"""
        await self._ensure_token()
        # HTTP 요청 + 에러 처리
```

**실전/모의 거래 모드 분리:**

```python
# 사용자가 KIS 인증 정보를 Real/Mock으로 분리 저장
user.kis_real_app_key       # 실전 거래용
user.kis_real_app_secret
user.kis_mock_app_key       # 모의 거래용
user.kis_mock_app_secret

# 요청 시 모드에 따라 자동 선택
mode = user.kis_trading_mode  # "REAL" or "MOCK"
client = KISClient(mode=mode)
```

#### 3.2 Market Data Service

**역할:** 시장 데이터 수집 및 저장

```python
class MarketDataService:
    async def collect_daily_data(
        self,
        symbol: str,
        start_date: date,
        end_date: date
    ):
        """일봉 데이터 수집"""
        # 1. KIS API로 데이터 요청
        # 2. MarketData 모델로 변환
        # 3. DB에 bulk insert
        # 4. 중복 처리 (UPSERT)
```

---

### 4. Data Access Layer (`models/`, `schemas/`, `db/`)

#### 4.1 Models (SQLAlchemy ORM)

**구조:**

```
models/
├── user.py          # 사용자 + KIS 인증 정보
├── strategy.py      # 전략 정의
├── signal.py        # 거래 신호
├── order.py         # 주문 기록
├── trade.py         # 체결 기록
├── holding.py       # 보유 종목
├── stock.py         # 종목 마스터
├── market_data.py   # OHLCV 데이터
├── watchlist.py     # 관심종목
└── backtest.py      # 백테스트 결과
```

**User 모델 예시:**

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))

    # KIS 실전 거래 인증
    kis_real_app_key = Column(String(255), nullable=True)
    kis_real_app_secret = Column(String(255), nullable=True)
    kis_real_account_number = Column(String(50), nullable=True)

    # KIS 모의 거래 인증
    kis_mock_app_key = Column(String(255), nullable=True)
    kis_mock_app_secret = Column(String(255), nullable=True)
    kis_mock_account_number = Column(String(50), nullable=True)

    # 거래 모드 선택
    kis_trading_mode = Column(
        Enum(TradingMode),
        default=TradingMode.MOCK
    )

    # Relationships
    strategies = relationship("Strategy", back_populates="user")
    orders = relationship("Order", back_populates="user")
```

**MarketData 모델 (시계열 데이터):**

```python
class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), index=True)
    timestamp = Column(DateTime(timezone=True), index=True)
    interval = Column(
        Enum(Interval),  # 1m, 5m, 10m, 30m, 1h, 1d
        index=True
    )

    # OHLCV
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=False)

    # Composite Index for fast queries
    __table_args__ = (
        Index('idx_symbol_interval_timestamp',
              'symbol', 'interval', 'timestamp'),
        UniqueConstraint('symbol', 'interval', 'timestamp'),
    )
```

#### 4.2 Schemas (Pydantic)

**역할:** API Request/Response 검증 및 직렬화

```python
# schemas/strategy.py
class StrategyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    strategy_type: StrategyType
    symbols: List[str]
    parameters: Dict[str, Any]
    is_active: bool = False

class StrategyCreate(StrategyBase):
    pass

class StrategyResponse(StrategyBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

#### 4.3 Database Session (`db/`)

**비동기 세션 관리:**

```python
# db/session.py
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """Dependency for getting DB session"""
    async with AsyncSessionLocal() as session:
        yield session
```

---

### 5. Core Utilities (`core/`)

#### 5.1 Security (`core/security.py`)

```python
# JWT 토큰 생성
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 비밀번호 해싱
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())
```

#### 5.2 Dependencies (`core/deps.py`)

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """현재 인증된 사용자 조회"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        # DB에서 사용자 조회
        return user
    except JWTError:
        raise HTTPException(401, "Invalid token")
```

---

## Frontend Architecture

### App Router 구조 (Next.js 14)

```
frontend/src/app/
├── layout.tsx           # Root Layout
├── page.tsx             # Home (Landing Page)
├── login/               # 로그인
├── register/            # 회원가입
├── dashboard/           # 대시보드
├── account/             # 계좌 정보
├── settings/            # KIS API 설정
├── market/              # 시장 데이터
├── stocks/              # 종목 탐색
├── strategies/          # 전략 관리
│   ├── page.tsx         # 전략 목록
│   ├── new/             # 전략 생성
│   └── [id]/            # 전략 상세
├── backtest/            # 백테스트
│   ├── page.tsx         # 백테스트 실행
│   └── [id]/            # 결과 조회
└── trades/              # 거래 내역
```

### 컴포넌트 구조

```
components/
├── layout/              # 레이아웃 컴포넌트
│   ├── DashboardLayout.tsx
│   ├── Navbar.tsx
│   └── Sidebar.tsx
├── auth/                # 인증 관련
│   └── ProtectedRoute.tsx
├── market/              # 시장 데이터
│   ├── MarketChart.tsx
│   └── MarketDataTable.tsx
├── strategy/            # 전략 관련
│   ├── StockSearchInput.tsx
│   └── MultiStockSelector.tsx
├── stocks/              # 종목 관련
│   └── StockSearchDialog.tsx
└── ui/                  # shadcn/ui 기본 컴포넌트
    ├── button.tsx
    ├── card.tsx
    ├── input.tsx
    ├── select.tsx
    ├── table.tsx
    └── ... (35+ components)
```

### API Client Layer

```
lib/
├── api.ts               # Axios 인스턴스 (Base)
├── authApi.ts           # Auth 엔드포인트
├── accountApi.ts        # Account 엔드포인트
├── dashboardApi.ts      # Dashboard 엔드포인트
├── strategyApi.ts       # Strategy 엔드포인트
├── stockApi.ts          # Stock 엔드포인트
└── watchlistApi.ts      # Watchlist 엔드포인트
```

**Axios 인스턴스 설정:**

```typescript
// lib/api.ts
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor (토큰 자동 삽입)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response Interceptor (에러 처리)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // 토큰 만료 → 리프레시 or 로그아웃
    }
    return Promise.reject(error);
  }
);
```

### State Management

**현재:** React Context API 사용

```typescript
// contexts/AuthContext.tsx
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 토큰 확인 및 사용자 정보 로드
    checkAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

**향후 확장:** Zustand or Redux Toolkit (필요 시)

---

## Database Design

### Entity Relationship Diagram

```
┌─────────────┐          ┌──────────────┐          ┌──────────────┐
│   Users     │          │  Strategies  │          │   Signals    │
├─────────────┤          ├──────────────┤          ├──────────────┤
│ id (PK)     │──1:N────▶│ id (PK)      │──1:N────▶│ id (PK)      │
│ email       │          │ user_id (FK) │          │ strategy_id  │
│ password    │          │ name         │          │ symbol       │
│ kis_real_*  │          │ type         │          │ signal_type  │
│ kis_mock_*  │          │ symbols      │          │ price        │
│ trading_mode│          │ parameters   │          │ timestamp    │
└─────────────┘          │ is_active    │          └──────────────┘
       │                 └──────────────┘                  │
       │                                                   │
       │                 ┌──────────────┐                 │
       │                 │   Orders     │◀────0:1─────────┘
       │                 ├──────────────┤
       └─────1:N────────▶│ id (PK)      │
                         │ user_id (FK) │
                         │ signal_id    │
                         │ symbol       │
                         │ order_type   │
                         │ quantity     │
                         │ price        │
                         │ status       │
                         └──────────────┘
                                │
                                │1:N
                                ▼
                         ┌──────────────┐
                         │   Trades     │
                         ├──────────────┤
                         │ id (PK)      │
                         │ order_id (FK)│
                         │ quantity     │
                         │ price        │
                         │ timestamp    │
                         └──────────────┘
```

**보조 테이블:**

```
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│   Stocks     │          │ Market Data  │          │  Watchlist   │
├──────────────┤          ├──────────────┤          ├──────────────┤
│ id (PK)      │          │ id (PK)      │          │ id (PK)      │
│ symbol (UK)  │          │ symbol       │          │ user_id (FK) │
│ name         │          │ timestamp    │          │ symbol       │
│ market_type  │          │ interval     │          │ name         │
│ sector       │          │ open/high/   │          │ notes        │
│ industry     │          │ low/close    │          └──────────────┘
│ market_cap   │          │ volume       │
└──────────────┘          └──────────────┘
```

### 주요 테이블 스키마

상세 스키마는 [DATABASE_SPECIFICATION.md](DATABASE_SPECIFICATION.md) 참조

**핵심 설계 원칙:**
1. ✅ 정규화: 3NF 준수
2. ✅ 인덱스: 조회 성능 최적화 (50+ indexes)
3. ✅ 제약조건: FK, Unique, Check constraints
4. ✅ 타임스탬프: created_at, updated_at 필수
5. ✅ Soft Delete: is_active 플래그 사용 (일부)

---

## Integration Points

### 1. Authentication Flow

```
Client                Frontend              Backend               Database
  │                     │                     │                      │
  │─────Login Request───▶│                     │                      │
  │                     │───POST /auth/login─▶│                      │
  │                     │                     │───Query User────────▶│
  │                     │                     │◀───User Data─────────│
  │                     │                     │                      │
  │                     │                     │ Verify Password      │
  │                     │                     │ Generate JWT Tokens  │
  │                     │                     │                      │
  │                     │◀───Tokens + User────│                      │
  │◀───Store in Local───│                     │                      │
  │     Storage         │                     │                      │
  │                     │                     │                      │
  │────Protected Req────▶│─────+ JWT Token────▶│                      │
  │                     │                     │ Verify Token         │
  │                     │                     │ Extract user_id      │
  │                     │                     │───Query User────────▶│
  │                     │                     │◀───User Data─────────│
  │                     │◀─────Response───────│                      │
  │◀───Display Data─────│                     │                      │
```

### 2. KIS API Integration

```
Backend              KIS Token Manager      KIS API (External)
  │                        │                      │
  │─Request Balance────────▶│                      │
  │                        │─Check Token Validity─│
  │                        │                      │
  │                        │  (If expired)        │
  │                        │───POST /oauth2/tokenP─▶
  │                        │◀───Access Token──────│
  │                        │  Save to DB          │
  │                        │                      │
  │◀─Valid Token───────────│                      │
  │                        │                      │
  │─────────────GET /uapi/domestic-stock/v1/trading/inquire-balance───▶
  │                                                │
  │                         Headers:               │
  │                         - authorization: Bearer {token}
  │                         - appkey, appsecret    │
  │                         - tr_id               │
  │                                                │
  │◀────────────────────Balance Data──────────────│
  │                                                │
  │  Parse & Return                               │
```

### 3. Strategy Execution Flow

```
User              Frontend          Backend API       Strategy Service    KIS API
 │                   │                  │                   │               │
 │─Click Execute─────▶│                  │                   │               │
 │                   │─POST /strategies/│                   │               │
 │                   │    {id}/execute  │                   │               │
 │                   │                  │─Load Strategy─────▶               │
 │                   │                  │                   │               │
 │                   │                  │◀─Strategy Object──│               │
 │                   │                  │                   │               │
 │                   │                  │─Get Market Data───▶               │
 │                   │                  │                   │─Query KIS API─▶
 │                   │                  │                   │◀─Price Data───│
 │                   │                  │◀─Market Data──────│               │
 │                   │                  │                   │               │
 │                   │                  │ Generate Signals  │               │
 │                   │                  │ (Strategy Engine) │               │
 │                   │                  │                   │               │
 │                   │                  │─Save Signals──────▶ DB            │
 │                   │                  │                   │               │
 │                   │                  │ (If auto-execute) │               │
 │                   │                  │─Place Order───────▶               │
 │                   │                  │                   │─POST Order────▶
 │                   │                  │                   │◀─Order Result─│
 │                   │◀─Success─────────│                   │               │
 │◀─Display Result───│                  │                   │               │
```

### 4. Market Data Collection

```
Scheduled Job       Backend Service        KIS API          Database
     │                    │                   │                │
     │─Trigger Daily──────▶│                   │                │
     │  Collection         │                   │                │
     │                    │─GET Stock List────▶ DB              │
     │                    │◀─Symbols──────────│                │
     │                    │                   │                │
     │                    │─For each symbol:  │                │
     │                    │                   │                │
     │                    │───GET OHLCV───────▶                │
     │                    │◀───Chart Data─────│                │
     │                    │                   │                │
     │                    │─Parse & Transform │                │
     │                    │                   │                │
     │                    │─UPSERT MarketData─▶                │
     │                    │  (Bulk Insert)    │                │
     │                    │◀─Success──────────│                │
     │                    │                   │                │
     │◀─Completion Report─│                   │                │
```

---

## Security Architecture

### 1. Authentication & Authorization

**Multi-Layer Security:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (Browser)                         │
│  - HTTPS Only                                               │
│  - JWT Token in localStorage                                │
│  - XSS Protection (Content-Security-Policy)                 │
└──────────────────────┬──────────────────────────────────────┘
                       │ TLS 1.3
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                            │
│  - CORS Configuration                                       │
│  - Rate Limiting (Future)                                   │
│  - Request Validation                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Middleware                         │
│  - JWT Verification                                         │
│  - User Authentication                                      │
│  - Permission Check                                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Business Logic                             │
│  - User Context Injection                                   │
│  - Resource Ownership Validation                            │
└─────────────────────────────────────────────────────────────┘
```

### 2. Credential Storage

**KIS API 인증 정보 보안:**

```python
# Database Storage (Encrypted at REST)
class User(Base):
    # 암호화 저장 (TODO: Implement encryption)
    kis_real_app_key = Column(String(255))      # AES-256 암호화 예정
    kis_real_app_secret = Column(String(255))   # AES-256 암호화 예정

    # 환경 변수로 암호화 키 관리
    # ENCRYPTION_KEY=... (32 bytes)
```

**권장 보안 조치:**

1. ✅ Database-level 암호화 (PostgreSQL 투명 데이터 암호화)
2. 🔄 Application-level 암호화 (cryptography 라이브러리)
3. 🔄 Key Management Service (AWS KMS, Azure Key Vault)
4. ✅ 환경 변수로 암호화 키 관리 (절대 코드에 하드코딩 금지)

### 3. API Security

**보안 헤더:**

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security Headers (향후 추가 권장)
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

### 4. Input Validation

**Pydantic을 통한 자동 검증:**

```python
class StrategyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    symbols: List[str] = Field(..., min_items=1, max_items=20)
    parameters: Dict[str, Any]

    @validator('symbols')
    def validate_symbols(cls, v):
        # SQL Injection 방지
        for symbol in v:
            if not symbol.isalnum():
                raise ValueError("Invalid symbol format")
        return v
```

---

## Deployment Architecture

### 현재 구성 (Development)

```
┌────────────────────────────────────────────────────────────┐
│                     Local Machine                          │
│                                                            │
│  ┌──────────────────┐      ┌──────────────────┐          │
│  │  Frontend        │      │  Backend         │          │
│  │  (npm run dev)   │      │  (uvicorn)       │          │
│  │  Port: 3000      │      │  Port: 8000      │          │
│  └──────────────────┘      └──────────────────┘          │
│                                      │                     │
│                                      ▼                     │
│                         ┌────────────────────┐            │
│                         │  PostgreSQL        │            │
│                         │  (Docker)          │            │
│                         │  Port: 5432        │            │
│                         └────────────────────┘            │
└────────────────────────────────────────────────────────────┘
```

### 프로덕션 구성 (예정)

```
                        ┌──────────────────┐
                        │   Load Balancer  │
                        │   (Nginx/ALB)    │
                        └────────┬─────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
         ┌────────────┐   ┌────────────┐  ┌────────────┐
         │ Frontend   │   │ Frontend   │  │ Frontend   │
         │ Container  │   │ Container  │  │ Container  │
         │ (Next.js)  │   │ (Next.js)  │  │ (Next.js)  │
         └─────┬──────┘   └─────┬──────┘  └─────┬──────┘
               │                │                │
               └────────────────┼────────────────┘
                                │
                                ▼
                        ┌───────────────┐
                        │ API Gateway   │
                        └───────┬───────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
         ┌────────────┐  ┌────────────┐  ┌────────────┐
         │ Backend    │  │ Backend    │  │ Backend    │
         │ Container  │  │ Container  │  │ Container  │
         │ (FastAPI)  │  │ (FastAPI)  │  │ (FastAPI)  │
         └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
               │               │               │
               └───────────────┼───────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │  PostgreSQL (RDS/Managed)    │
                │  - Read Replicas             │
                │  - Automated Backups         │
                └──────────────────────────────┘
```

**컨테이너 구성 (docker-compose.yml):**

```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/trading_db
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=trading_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## API Documentation

### OpenAPI/Swagger

**자동 생성 문서:** http://localhost:8000/docs

**주요 API 그룹:**

| 그룹 | Base Path | 엔드포인트 수 | 인증 필요 |
|------|-----------|-------------|----------|
| Authentication | `/api/v1/auth` | 5 | 일부 |
| Account | `/api/v1/account` | 6 | ✓ |
| Market | `/api/v1/market` | 5 | ✓ |
| Strategy | `/api/v1/strategies` | 8 | ✓ |
| Stocks | `/api/v1/stocks` | 4 | ✓ |
| Watchlist | `/api/v1/watchlists` | 5 | ✓ |
| Dashboard | `/api/v1/dashboard` | 1 | ✓ |
| Backtest | `/api/v1/backtest` | 3 | ✓ |

**예시 API 명세:**

```yaml
paths:
  /api/v1/strategies:
    get:
      summary: Get all strategies
      tags: [Strategy]
      security:
        - bearerAuth: []
      responses:
        200:
          description: List of strategies
          content:
            application/json:
              schema:
                type: object
                properties:
                  total:
                    type: integer
                  strategies:
                    type: array
                    items:
                      $ref: '#/components/schemas/Strategy'

    post:
      summary: Create strategy
      tags: [Strategy]
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StrategyCreate'
      responses:
        201:
          description: Strategy created
```

---

## 향후 개선 계획

### Phase 1: 핵심 기능 완성 (Sprint 3)

- ✅ Backtest Engine 구현
- ✅ Account stub endpoints 완성
- ✅ 단위/통합 테스트 추가

### Phase 2: 보안 & 성능 (Sprint 4)

- 🔄 Redis 토큰 블랙리스트
- 🔄 Rate Limiting 구현
- 🔄 API 암호화 강화 (AES-256)
- 🔄 Connection Pooling 최적화

### Phase 3: 확장성 (Sprint 5+)

- 🔄 WebSocket 실시간 시세 연동
- 🔄 Celery 백그라운드 작업 큐
- 🔄 Redis 캐싱 레이어
- 🔄 Microservices 분리 (Strategy Engine 독립)

### Phase 4: 모니터링 & 운영

- 🔄 Prometheus + Grafana 모니터링
- 🔄 ELK Stack 로깅 집계
- 🔄 Sentry 에러 트래킹
- 🔄 APM (Application Performance Monitoring)

---

**문서 버전:** 1.0
**최종 업데이트:** 2025-11-12
**다음 리뷰:** Sprint 3 완료 시점

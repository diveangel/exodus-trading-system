# Exodus Trading System - 개발환경 정보

## 프로젝트 개요
한국투자증권 API를 활용한 자동 매매 시스템

## 기술 스택

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Database**: PostgreSQL 15 (Docker)
- **ORM**: SQLAlchemy 2.0+ (Async)
- **Authentication**: JWT (JSON Web Tokens)
- **API Client**: httpx (Async HTTP client)
- **Testing**: pytest (Async support)
- **Password Hashing**: bcrypt

### Frontend
- **Framework**: Next.js 14.2.33 (App Router)
- **Language**: TypeScript
- **UI Library**: React 18
- **Styling**: Tailwind CSS
- **Component Library**: shadcn/ui
- **HTTP Client**: Axios
- **Form Validation**: React Hook Form + Zod
- **Icons**: Lucide React

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database Container**: postgres:15-alpine

## 디렉토리 구조

```
exodus-trading-system/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── account.py       # 계좌 관리 API
│   │   │       ├── auth.py          # 인증 API
│   │   │       └── dashboard.py     # 대시보드 API
│   │   ├── core/
│   │   │   ├── config.py            # 설정
│   │   │   ├── deps.py              # 의존성
│   │   │   └── security.py          # 보안 (JWT, 암호화)
│   │   ├── db/
│   │   │   ├── base.py              # SQLAlchemy Base
│   │   │   └── session.py           # DB 세션
│   │   ├── models/
│   │   │   └── user.py              # User 모델
│   │   ├── schemas/
│   │   │   └── user.py              # Pydantic 스키마
│   │   ├── services/
│   │   │   └── kis_client.py        # KIS API 클라이언트
│   │   └── main.py                  # FastAPI 앱
│   ├── tests/
│   │   └── test_kis_api.py          # KIS API 테스트
│   ├── venv/                        # Python 가상환경
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── account/             # 계좌 정보 페이지
│   │   │   ├── dashboard/           # 대시보드
│   │   │   ├── login/               # 로그인
│   │   │   ├── register/            # 회원가입
│   │   │   ├── settings/            # 설정 (KIS API 연동)
│   │   │   ├── strategies/          # 전략 관리
│   │   │   └── trades/              # 거래 내역
│   │   ├── components/
│   │   │   ├── layout/              # 레이아웃 컴포넌트
│   │   │   └── ui/                  # UI 컴포넌트 (shadcn)
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx      # 인증 Context
│   │   └── lib/
│   │       ├── api.ts               # Axios 인스턴스
│   │       ├── accountApi.ts        # 계좌 API 클라이언트
│   │       └── authApi.ts           # 인증 API 클라이언트
│   ├── public/
│   └── package.json
└── docker-compose.yml               # PostgreSQL 컨테이너 설정
```

## 환경 설정

### Backend 환경변수 (.env)
```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/trading_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend 환경변수 (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 서버 실행

### Backend 서버
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- URL: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Frontend 서버
```bash
cd frontend
npm run dev
```
- URL: http://localhost:3001 (포트 3000이 사용 중이면 자동으로 3001 사용)

### Database (Docker)
```bash
docker-compose up -d
```
- PostgreSQL: localhost:5432
- Container: exodus-postgres

## 데이터베이스 스키마

### Users 테이블
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'USER',

    -- KIS API 인증 정보
    kis_app_key VARCHAR(255),
    kis_app_secret VARCHAR(255),
    kis_account_number VARCHAR(50),
    kis_account_code VARCHAR(10),
    kis_trading_mode VARCHAR(10) NOT NULL DEFAULT 'MOCK',  -- MOCK 또는 REAL
    has_kis_credentials BOOLEAN NOT NULL DEFAULT FALSE,

    -- 상태
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,

    -- 타임스탬프
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

### Enums
- **UserRole**: ADMIN, USER, VIEWER
- **TradingMode**: MOCK (모의투자), REAL (실전투자)

## API 엔드포인트

### 인증 (Authentication)
- `POST /api/v1/auth/register` - 회원가입
- `POST /api/v1/auth/login` - 로그인
- `POST /api/v1/auth/logout` - 로그아웃
- `GET /api/v1/auth/me` - 현재 사용자 정보
- `POST /api/v1/auth/refresh` - 토큰 갱신

### 대시보드 (Dashboard)
- `GET /api/v1/dashboard` - 대시보드 데이터 조회

### 계좌 (Account)
- `GET /api/v1/account/balance` - 계좌 잔고 조회 (KIS API 연동)
- `GET /api/v1/account/kis-credentials` - KIS 인증 정보 조회 (마스킹)
- `PUT /api/v1/account/kis-credentials` - KIS 인증 정보 업데이트
- `DELETE /api/v1/account/kis-credentials` - KIS 인증 정보 삭제

## 한국투자증권 API 연동

### 거래 모드 설정
사용자는 Settings 페이지에서 다음 두 가지 모드 중 하나를 선택할 수 있습니다:
- **모의투자 (MOCK)**: 실제 자금 없이 거래 테스트 (기본값)
  - URL: https://openapivts.koreainvestment.com:29443
- **실전투자 (REAL)**: 실제 계좌로 거래 실행
  - URL: https://openapi.koreainvestment.com:9443

### KIS API 클라이언트 기능
- OAuth 토큰 발급 및 자동 갱신
- 계좌 잔고 조회
- 현재가 조회
- 주문 실행 (매수/매도)
- 주문 내역 조회

## 개발 상태

### 완료된 기능
- ✅ 사용자 인증 (회원가입, 로그인, JWT)
- ✅ KIS API 인증 정보 관리 (Settings 페이지)
- ✅ 계좌 잔고 조회 (실시간 KIS API 연동)
- ✅ 대시보드 (Mock 데이터)
- ✅ 모의투자/실전투자 모드 선택 기능
- ✅ TDD 방식 KIS API 테스트 (7개 테스트 통과)

### 진행 중
- 🔄 KIS API 403 Forbidden 오류 해결 필요
  - 현재 로그인은 성공하지만 계좌 정보 조회 시 KIS API에서 403 오류 발생
  - App Key와 App Secret 재확인 필요

### 구현 예정
- ⏳ Holdings (보유 종목) API 연동
- ⏳ Trades (거래 내역) API 연동
- ⏳ Orders (주문 내역) API 연동
- ⏳ 전략 관리 (Strategies)
- ⏳ 백테스팅 (Backtesting)

## 알려진 이슈

### 1. KIS API 403 Forbidden
- **증상**: 계좌 잔고 조회 시 403 오류 발생
- **원인**: KIS API 인증 정보 또는 권한 문제
- **해결 방법**:
  1. KIS 포털에서 발급받은 App Key와 App Secret 재확인
  2. 모의투자 계좌 활성화 여부 확인
  3. API 사용 권한 확인

### 2. Database Enum 값 불일치
- **증상**: 'mock' is not among the defined enum values (MOCK, REAL)
- **원인**: 데이터베이스에 소문자 'mock' 값이 저장되어 있으나 Enum은 대문자 'MOCK' 정의
- **해결 방법**: 데이터베이스의 기존 값을 대문자로 업데이트
  ```sql
  UPDATE users SET kis_trading_mode = 'MOCK' WHERE kis_trading_mode = 'mock';
  UPDATE users SET kis_trading_mode = 'REAL' WHERE kis_trading_mode = 'real';
  ```

## 테스트 계정

### 테스트 사용자
- Email: diveangel84@gmail.com
- KIS 계좌: 50156093-01
- Trading Mode: MOCK (모의투자)

## KIS API 정보 검색 가이드

KIS API 관련 정보를 찾을 때는 다음 순서로 검색하세요:

### 1순위: KIS 공식 GitHub
- **URL**: https://github.com/koreainvestment/open-trading-api/
- **주요 디렉토리**: `examples_llm/` (LLM 최적화 예제)
- **추천 이유**:
  - 가장 정확하고 최신의 공식 예제 코드
  - API 파라미터, TR ID, 응답 구조 등이 명확하게 정의됨
  - 각 API별로 독립된 디렉토리 구조

**예시 검색 경로:**
```
examples_llm/domestic_stock/inquire_balance/inquire_balance.py
examples_llm/domestic_stock/get_current_price/get_current_price.py
examples_llm/overseas_stock/get_stock_price/get_stock_price.py
```

### 2순위: KIS MCP 서버
- **설정 파일**: `.claude/mcp.json`
- **서버 URL**: https://server.smithery.ai/@KISOpenAPI/kis-code-assistant-mcp/mcp
- **제공 도구**:
  - `search_auth_api` - 인증 관련 API
  - `search_domestic_stock_api` - 국내 주식 API
  - `search_overseas_stock_api` - 해외 주식 API
  - 기타 채권, 선물/옵션, ELW API 검색
- **장점**: 자연어로 API 검색 및 코드 생성 지원

### 3순위: 웹 검색
- 위 두 방법으로 정보를 찾을 수 없을 때만 사용
- 검색 키워드 예시:
  - "한국투자증권 KIS API {기능명} 예제"
  - "KIS Open API {TR_ID} 파라미터"
  - "site:github.com/koreainvestment {검색어}"

### 중요 참고사항

1. **API 파라미터 확인**: GitHub 예제의 `params` 딕셔너리를 정확히 따를 것
2. **TR ID 구분**: 모의투자(V로 시작)와 실전투자(T로 시작) TR ID가 다름
3. **응답 구조**: 대부분 `output1`, `output2` 형태로 반환됨
4. **에러 처리**: `rt_cd`, `msg_cd`, `msg1` 필드로 에러 확인

## 참고 문서

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Next.js 공식 문서](https://nextjs.org/docs)
- [한국투자증권 OpenAPI 문서](https://apiportal.koreainvestment.com/)
- [KIS 공식 GitHub](https://github.com/koreainvestment/open-trading-api/)
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/en/20/)

## 개발 도구

- **Backend IDE**: Visual Studio Code
- **Version Control**: Git
- **Python Package Manager**: pip
- **Node Package Manager**: npm
- **Database Client**: PostgreSQL CLI / Docker Desktop

## 최종 업데이트
2025-11-03

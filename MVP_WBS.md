# Exodus Trading System MVP - WBS (Work Breakdown Structure)

**프로젝트명:** Exodus Trading System MVP
**작성일:** 2025-11-02
**버전:** 1.0
**목표 기간:** 8-10주

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [WBS 구조](#2-wbs-구조)
3. [Phase 1: 인프라 구축](#phase-1-인프라-구축-완료)
4. [Phase 2: 백엔드 핵심 기능](#phase-2-백엔드-핵심-기능)
5. [Phase 3: 프론트엔드 구현](#phase-3-프론트엔드-구현)
6. [Phase 4: 통합 및 테스트](#phase-4-통합-및-테스트)
7. [일정 및 마일스톤](#일정-및-마일스톤)
8. [리스크 관리](#리스크-관리)

---

## 1. 프로젝트 개요

### 1.1 MVP 목표

한국투자증권 API를 연동하여 간단한 모멘텀 전략을 실행하고 백테스트할 수 있는 최소 기능 제품 개발

### 1.2 MVP 범위

- ✅ JWT 인증 시스템
- ✅ 사용자 관리
- ✅ 한국투자증권 API 연동
- ✅ 간단한 모멘텀 전략 (이동평균 교차)
- ✅ 백테스트 엔진
- ✅ 기본 웹 인터페이스

### 1.3 제외 사항 (Phase 2 이후)

- ❌ 실시간 자동매매
- ❌ WebSocket 실시간 업데이트
- ❌ 복잡한 투자 전략
- ❌ 고급 리스크 관리
- ❌ 상세 대시보드

---

## 2. WBS 구조

```
1.0 Exodus Trading System MVP
│
├── 1.1 프로젝트 관리
│   ├── 1.1.1 요구사항 정의 [완료]
│   ├── 1.1.2 아키텍처 설계 [완료]
│   └── 1.1.3 문서화 [진행중]
│
├── 1.2 인프라 구축 [완료]
│   ├── 1.2.1 프로젝트 구조 생성
│   ├── 1.2.2 Docker 환경 설정
│   ├── 1.2.3 데이터베이스 모델 설계
│   └── 1.2.4 개발 환경 구성
│
├── 1.3 백엔드 개발
│   ├── 1.3.1 데이터베이스 구축
│   ├── 1.3.2 인증 시스템
│   ├── 1.3.3 한국투자증권 API 연동
│   ├── 1.3.4 전략 엔진
│   ├── 1.3.5 백테스트 엔진
│   └── 1.3.6 API 엔드포인트 구현
│
├── 1.4 프론트엔드 개발
│   ├── 1.4.1 인증 UI
│   ├── 1.4.2 전략 관리 UI
│   ├── 1.4.3 백테스트 UI
│   └── 1.4.4 계좌 정보 UI
│
├── 1.5 통합 및 테스트
│   ├── 1.5.1 단위 테스트
│   ├── 1.5.2 통합 테스트
│   ├── 1.5.3 E2E 테스트
│   └── 1.5.4 성능 테스트
│
└── 1.6 배포 및 운영
    ├── 1.6.1 Docker 배포
    ├── 1.6.2 모니터링 설정
    └── 1.6.3 문서화 완료
```

---

## Phase 1: 인프라 구축 [완료]

### ✅ 1.2.1 프로젝트 구조 생성

**상태:** 완료
**소요 시간:** 2시간
**완료일:** 2025-11-01

**세부 작업:**
- [x] Backend 디렉토리 구조 생성
- [x] Frontend 디렉토리 구조 생성
- [x] 설정 파일 생성 (.gitignore, .env.example)
- [x] README 작성

**산출물:**
- 프로젝트 디렉토리 구조
- 기본 설정 파일

---

### ✅ 1.2.2 Docker 환경 설정

**상태:** 완료
**소요 시간:** 3시간
**완료일:** 2025-11-01

**세부 작업:**
- [x] Backend Dockerfile 작성
- [x] Frontend Dockerfile 작성
- [x] docker-compose.yml 작성
- [x] Nginx 설정
- [x] PostgreSQL 컨테이너 설정
- [x] Redis 컨테이너 설정

**산출물:**
- Docker 설정 파일
- docker-compose.yml
- nginx.conf

---

### ✅ 1.2.3 데이터베이스 모델 설계

**상태:** 완료
**소요 시간:** 6시간
**완료일:** 2025-11-02

**세부 작업:**
- [x] User 모델 및 스키마
- [x] Strategy 모델 및 스키마
- [x] Signal 모델 및 스키마
- [x] Order/Trade 모델 및 스키마
- [x] Holding 모델 및 스키마
- [x] MarketData 모델 및 스키마
- [x] Backtest 모델 및 스키마
- [x] 데이터베이스 명세서 작성

**산출물:**
- SQLAlchemy 모델 (9개)
- Pydantic 스키마 (각 모델당 3-5개)
- DATABASE_SPECIFICATION.md

---

### ✅ 1.2.4 개발 환경 구성

**상태:** 완료
**소요 시간:** 2시간
**완료일:** 2025-11-01

**세부 작업:**
- [x] Python 가상환경 설정
- [x] requirements.txt 작성
- [x] Node.js 패키지 설정
- [x] package.json 작성
- [x] TypeScript 설정
- [x] Linting 및 Formatting 설정

**산출물:**
- requirements.txt
- package.json
- tsconfig.json

---

## Phase 2: 백엔드 핵심 기능

### 🔄 1.3.1 데이터베이스 구축

**상태:** 준비
**예상 소요 시간:** 3시간
**우선순위:** 높음
**담당:** Backend

**세부 작업:**
- [ ] 1.3.1.1 Alembic 마이그레이션 생성
- [ ] 1.3.1.2 마이그레이션 실행 및 테스트
- [ ] 1.3.1.3 초기 데이터 Seed 작성 (선택)
- [ ] 1.3.1.4 데이터베이스 연결 테스트

**의존성:** 1.2.3 (데이터베이스 모델 설계)

**산출물:**
- Alembic 마이그레이션 파일
- 데이터베이스 스키마

**검증 기준:**
- 모든 테이블이 정상적으로 생성됨
- 외래키 제약조건이 올바르게 설정됨
- 인덱스가 생성됨

---

### 🔄 1.3.2 인증 시스템

**상태:** 준비
**예상 소요 시간:** 8시간
**우선순위:** 높음
**담당:** Backend

#### 1.3.2.1 JWT 인증 구현 (3시간)

**세부 작업:**
- [ ] JWT 토큰 생성 함수 구현
- [ ] JWT 토큰 검증 함수 구현
- [ ] Refresh Token 관리 (Redis)
- [ ] 토큰 갱신 로직

**산출물:**
- `app/utils/security.py` (완료)
- `app/utils/jwt.py`

#### 1.3.2.2 사용자 인증 API (5시간)

**세부 작업:**
- [ ] POST /auth/register - 회원가입
  - 이메일 검증
  - 비밀번호 해싱
  - 사용자 생성
- [ ] POST /auth/login - 로그인
  - 이메일/비밀번호 검증
  - JWT 토큰 발급
- [ ] POST /auth/logout - 로그아웃
  - Refresh Token 무효화
- [ ] POST /auth/refresh - 토큰 갱신
- [ ] GET /auth/me - 현재 사용자 조회
- [ ] 인증 Dependency 구현

**산출물:**
- `app/api/v1/auth.py`
- `app/services/user_service.py`
- `app/middleware/auth.py`

**검증 기준:**
- 회원가입 시 이메일 중복 검증
- 로그인 실패 시 적절한 에러 메시지
- 토큰 만료 시 자동 갱신
- 보호된 엔드포인트 접근 제어

---

### 🔄 1.3.3 한국투자증권 API 연동

**상태:** 준비
**예상 소요 시간:** 12시간
**우선순위:** 높음
**담당:** Backend

#### 1.3.3.1 KIS API 클라이언트 구현 (6시간)

**세부 작업:**
- [ ] API 인증 (App Key, Secret)
- [ ] Access Token 발급 및 갱신
- [ ] API 호출 기본 클래스
- [ ] 에러 핸들링
- [ ] Rate Limiting 처리

**산출물:**
- `app/services/kis/client.py`
- `app/services/kis/auth.py`
- `app/services/kis/exceptions.py`

#### 1.3.3.2 시장 데이터 수집 (3시간)

**세부 작업:**
- [ ] 현재가 조회
- [ ] 일봉 데이터 조회
- [ ] 종목 정보 조회
- [ ] 데이터 파싱 및 저장

**산출물:**
- `app/services/kis/market_data.py`
- `app/services/market_data_service.py`

#### 1.3.3.3 계좌 조회 기능 (3시간)

**세부 작업:**
- [ ] 계좌 잔액 조회
- [ ] 보유 종목 조회
- [ ] 주문 내역 조회
- [ ] 데이터 동기화

**산출물:**
- `app/services/kis/account.py`
- `app/services/account_service.py`

**검증 기준:**
- API 인증 성공
- 시장 데이터 정상 수집
- 계좌 정보 정확히 조회

---

### 🔄 1.3.4 전략 엔진

**상태:** 준비
**예상 소요 시간:** 10시간
**우선순위:** 높음
**담당:** Backend

#### 1.3.4.1 전략 기본 클래스 (3시간)

**세부 작업:**
- [ ] 전략 Base 클래스 설계
- [ ] 전략 실행 인터페이스
- [ ] 신호 생성 인터페이스
- [ ] 파라미터 검증

**산출물:**
- `app/core/strategy/base.py`
- `app/core/strategy/types.py`

#### 1.3.4.2 모멘텀 전략 구현 (5시간)

**세부 작업:**
- [ ] 이동평균선 계산 (SMA, EMA)
- [ ] 이동평균 교차 전략
- [ ] 신호 생성 로직
- [ ] 신호 검증 및 필터링

**산출물:**
- `app/core/strategy/momentum.py`
- `app/core/indicators/moving_average.py`

#### 1.3.4.3 전략 관리 API (2시간)

**세부 작업:**
- [ ] GET /strategies - 전략 목록
- [ ] POST /strategies - 전략 생성
- [ ] GET /strategies/{id} - 전략 상세
- [ ] PUT /strategies/{id} - 전략 수정
- [ ] DELETE /strategies/{id} - 전략 삭제
- [ ] POST /strategies/{id}/run - 전략 실행

**산출물:**
- `app/api/v1/strategy.py`
- `app/services/strategy_service.py`

**검증 기준:**
- 이동평균 계산 정확성
- 신호 생성 로직 검증
- 전략 CRUD 동작

---

### 🔄 1.3.5 백테스트 엔진

**상태:** 준비
**예상 소요 시간:** 12시간
**우선순위:** 높음
**담당:** Backend

#### 1.3.5.1 백테스트 엔진 코어 (6시간)

**세부 작업:**
- [ ] 백테스트 실행 프레임워크
- [ ] 과거 데이터 로딩
- [ ] 일별 시뮬레이션 루프
- [ ] 주문 실행 시뮬레이션
- [ ] 포지션 관리
- [ ] 수수료/세금 계산

**산출물:**
- `app/core/backtest/engine.py`
- `app/core/backtest/portfolio.py`
- `app/core/backtest/executor.py`

#### 1.3.5.2 성과 지표 계산 (4시간)

**세부 작업:**
- [ ] 총 수익률 계산
- [ ] 연환산 수익률
- [ ] 최대 낙폭 (MDD)
- [ ] 샤프 지수
- [ ] 승률 및 손익비
- [ ] 거래 통계

**산출물:**
- `app/core/backtest/metrics.py`
- `app/core/backtest/analyzer.py`

#### 1.3.5.3 백테스트 API (2시간)

**세부 작업:**
- [ ] POST /backtest/run - 백테스트 실행
- [ ] GET /backtest/results/{id} - 결과 조회
- [ ] GET /backtest/history - 백테스트 이력

**산출물:**
- `app/api/v1/backtest.py`
- `app/services/backtest_service.py`

**검증 기준:**
- 백테스트 실행 성공
- 성과 지표 정확성
- 결과 저장 및 조회

---

### 🔄 1.3.6 API 엔드포인트 구현

**상태:** 준비
**예상 소요 시간:** 6시간
**우선순위:** 중간
**담당:** Backend

#### 1.3.6.1 계좌 API (2시간)

**세부 작업:**
- [ ] GET /account/balance - 잔액 조회
- [ ] GET /account/holdings - 보유 종목
- [ ] GET /account/trades - 거래 내역
- [ ] GET /account/profit-loss - 손익 조회

**산출물:**
- `app/api/v1/account.py` (업데이트)

#### 1.3.6.2 시장 데이터 API (2시간)

**세부 작업:**
- [ ] GET /market/price/{symbol} - 현재가
- [ ] GET /market/chart/{symbol} - 차트 데이터
- [ ] GET /market/search - 종목 검색

**산출물:**
- `app/api/v1/market.py` (업데이트)

#### 1.3.6.3 API 문서화 (2시간)

**세부 작업:**
- [ ] OpenAPI 스키마 검증
- [ ] API 예제 작성
- [ ] 에러 코드 정의

**산출물:**
- Swagger UI 문서
- API 사용 가이드

---

## Phase 3: 프론트엔드 구현

### 🔄 1.4.1 인증 UI

**상태:** 준비
**예상 소요 시간:** 8시간
**우선순위:** 높음
**담당:** Frontend

#### 1.4.1.1 인증 페이지 (4시간)

**세부 작업:**
- [ ] 로그인 페이지 (`/login`)
- [ ] 회원가입 페이지 (`/register`)
- [ ] 폼 검증
- [ ] 에러 처리

**산출물:**
- `frontend/src/app/login/page.tsx`
- `frontend/src/app/register/page.tsx`
- `frontend/src/components/auth/LoginForm.tsx`
- `frontend/src/components/auth/RegisterForm.tsx`

#### 1.4.1.2 인증 상태 관리 (2시간)

**세부 작업:**
- [ ] 인증 상태 스토어 (Zustand)
- [ ] 로그인/로그아웃 액션
- [ ] 토큰 저장 및 관리
- [ ] Protected Route 구현

**산출물:**
- `frontend/src/store/authStore.ts`
- `frontend/src/components/auth/ProtectedRoute.tsx`

#### 1.4.1.3 레이아웃 구성 (2시간)

**세부 작업:**
- [ ] 네비게이션 바
- [ ] 사이드바
- [ ] 사용자 메뉴
- [ ] 로그아웃 버튼

**산출물:**
- `frontend/src/components/layout/Navbar.tsx`
- `frontend/src/components/layout/Sidebar.tsx`

**검증 기준:**
- 로그인/회원가입 동작
- 토큰 자동 갱신
- Protected Route 접근 제어

---

### 🔄 1.4.2 전략 관리 UI

**상태:** 준비
**예상 소요 시간:** 10시간
**우선순위:** 높음
**담당:** Frontend

#### 1.4.2.1 전략 목록 페이지 (3시간)

**세부 작업:**
- [ ] 전략 목록 표시
- [ ] 전략 카드 컴포넌트
- [ ] 필터링 및 정렬
- [ ] 전략 상태 토글

**산출물:**
- `frontend/src/app/strategies/page.tsx`
- `frontend/src/components/strategy/StrategyList.tsx`
- `frontend/src/components/strategy/StrategyCard.tsx`

#### 1.4.2.2 전략 생성/수정 폼 (4시간)

**세부 작업:**
- [ ] 전략 생성 폼
- [ ] 파라미터 입력 필드
- [ ] 전략 타입 선택
- [ ] 폼 검증

**산출물:**
- `frontend/src/components/strategy/StrategyForm.tsx`
- `frontend/src/components/strategy/ParameterInput.tsx`

#### 1.4.2.3 전략 상세 페이지 (3시간)

**세부 작업:**
- [ ] 전략 정보 표시
- [ ] 파라미터 표시
- [ ] 백테스트 실행 버튼
- [ ] 전략 수정/삭제

**산출물:**
- `frontend/src/app/strategies/[id]/page.tsx`
- `frontend/src/components/strategy/StrategyDetail.tsx`

**검증 기준:**
- 전략 CRUD 동작
- 파라미터 입력 검증
- UI/UX 직관성

---

### 🔄 1.4.3 백테스트 UI

**상태:** 준비
**예상 소요 시간:** 12시간
**우선순위:** 높음
**담당:** Frontend

#### 1.4.3.1 백테스트 실행 페이지 (4시간)

**세부 작업:**
- [ ] 백테스트 설정 폼
- [ ] 기간 선택 (DatePicker)
- [ ] 초기 자본금 입력
- [ ] 전략 선택
- [ ] 실행 버튼 및 진행 상태

**산출물:**
- `frontend/src/app/backtest/page.tsx`
- `frontend/src/components/backtest/BacktestForm.tsx`

#### 1.4.3.2 백테스트 결과 페이지 (6시간)

**세부 작업:**
- [ ] 성과 지표 카드
- [ ] 수익률 차트 (Recharts)
- [ ] 거래 내역 테이블
- [ ] MDD 차트
- [ ] 거래 통계 표시

**산출물:**
- `frontend/src/app/backtest/[id]/page.tsx`
- `frontend/src/components/backtest/BacktestResults.tsx`
- `frontend/src/components/backtest/PerformanceMetrics.tsx`
- `frontend/src/components/backtest/EquityCurve.tsx`
- `frontend/src/components/backtest/TradeHistory.tsx`

#### 1.4.3.3 백테스트 이력 페이지 (2시간)

**세부 작업:**
- [ ] 백테스트 이력 목록
- [ ] 필터링 및 정렬
- [ ] 결과 비교 기능

**산출물:**
- `frontend/src/app/backtest/history/page.tsx`
- `frontend/src/components/backtest/BacktestHistory.tsx`

**검증 기준:**
- 백테스트 실행 성공
- 차트 정상 렌더링
- 성과 지표 정확히 표시

---

### 🔄 1.4.4 계좌 정보 UI

**상태:** 준비
**예상 소요 시간:** 6시간
**우선순위:** 중간
**담당:** Frontend

#### 1.4.4.1 계좌 요약 페이지 (3시간)

**세부 작업:**
- [ ] 잔액 표시
- [ ] 총 자산 표시
- [ ] 손익 요약
- [ ] 자산 배분 차트

**산출물:**
- `frontend/src/app/account/page.tsx`
- `frontend/src/components/account/AccountSummary.tsx`
- `frontend/src/components/account/AssetAllocation.tsx`

#### 1.4.4.2 보유 종목 페이지 (3시간)

**세부 작업:**
- [ ] 보유 종목 테이블
- [ ] 평가 손익 표시
- [ ] 종목별 비중
- [ ] 정렬 및 필터링

**산출물:**
- `frontend/src/app/holdings/page.tsx`
- `frontend/src/components/holding/HoldingList.tsx`

**검증 기준:**
- 계좌 정보 정확히 표시
- 실시간 데이터 반영 (새로고침)

---

## Phase 4: 통합 및 테스트

### 🔄 1.5.1 단위 테스트

**상태:** 준비
**예상 소요 시간:** 8시간
**우선순위:** 중간
**담당:** Backend/Frontend

#### Backend 단위 테스트 (5시간)

**세부 작업:**
- [ ] User Service 테스트
- [ ] Strategy Service 테스트
- [ ] Backtest Engine 테스트
- [ ] KIS API Client 테스트 (Mock)
- [ ] 유틸리티 함수 테스트

**산출물:**
- `backend/tests/test_services/`
- `backend/tests/test_core/`
- `backend/tests/test_utils/`

#### Frontend 단위 테스트 (3시간)

**세부 작업:**
- [ ] 컴포넌트 테스트
- [ ] 상태 관리 테스트
- [ ] API 클라이언트 테스트

**산출물:**
- `frontend/src/__tests__/`

**목표 커버리지:** 70% 이상

---

### 🔄 1.5.2 통합 테스트

**상태:** 준비
**예상 소요 시간:** 6시간
**우선순위:** 높음
**담당:** Backend

**세부 작업:**
- [ ] API 엔드포인트 통합 테스트
- [ ] 데이터베이스 트랜잭션 테스트
- [ ] 인증 플로우 테스트
- [ ] 백테스트 전체 플로우 테스트

**산출물:**
- `backend/tests/test_integration/`

**검증 기준:**
- 모든 API 엔드포인트 정상 동작
- 데이터 무결성 유지

---

### 🔄 1.5.3 E2E 테스트

**상태:** 준비
**예상 소요 시간:** 6시간
**우선순위:** 중간
**담당:** Frontend

**세부 작업:**
- [ ] 회원가입 플로우
- [ ] 로그인 플로우
- [ ] 전략 생성 플로우
- [ ] 백테스트 실행 플로우

**산출물:**
- E2E 테스트 스크립트

**도구:** Playwright or Cypress

---

### 🔄 1.5.4 성능 테스트

**상태:** 준비
**예상 소요 시간:** 4시간
**우선순위:** 낮음
**담당:** Backend

**세부 작업:**
- [ ] API 응답 시간 측정
- [ ] 백테스트 실행 시간 측정
- [ ] 데이터베이스 쿼리 최적화
- [ ] 부하 테스트

**산출물:**
- 성능 테스트 보고서

**목표:**
- API 응답 시간 < 500ms
- 백테스트 (10년) < 5분

---

## Phase 5: 배포 및 운영

### 🔄 1.6.1 Docker 배포

**상태:** 준비
**예상 소요 시간:** 4시간
**우선순위:** 높음
**담당:** DevOps

**세부 작업:**
- [ ] 프로덕션 환경 변수 설정
- [ ] Docker 이미지 최적화
- [ ] Docker Compose 프로덕션 설정
- [ ] 데이터 볼륨 백업 설정

**산출물:**
- `docker-compose.prod.yml`
- 배포 가이드

---

### 🔄 1.6.2 모니터링 설정

**상태:** 준비
**예상 소요 시간:** 3시간
**우선순위:** 중간
**담당:** DevOps

**세부 작업:**
- [ ] 로그 수집 설정
- [ ] 에러 트래킹 (Sentry, 선택)
- [ ] 헬스 체크 엔드포인트
- [ ] Docker 컨테이너 모니터링

**산출물:**
- 모니터링 대시보드
- 알림 설정

---

### 🔄 1.6.3 문서화 완료

**상태:** 진행중
**예상 소요 시간:** 4시간
**우선순위:** 중간
**담당:** All

**세부 작업:**
- [x] README.md 업데이트
- [x] DATABASE_SPECIFICATION.md
- [x] MVP_WBS.md
- [ ] API 사용 가이드
- [ ] 배포 가이드
- [ ] 사용자 매뉴얼

**산출물:**
- 완성된 문서 세트

---

## 일정 및 마일스톤

### 전체 일정 (8-10주)

| Phase | 기간 | 기간 |
|-------|------|------|
| Phase 1: 인프라 구축 | Week 1 | ✅ 완료 |
| Phase 2: 백엔드 핵심 기능 | Week 2-5 | 4주 |
| Phase 3: 프론트엔드 구현 | Week 5-7 | 3주 |
| Phase 4: 통합 및 테스트 | Week 7-8 | 2주 |
| Phase 5: 배포 및 운영 | Week 9-10 | 2주 |

### 주요 마일스톤

| 마일스톤 | 목표일 | 달성 기준 |
|----------|--------|----------|
| M1: 인프라 완료 | Week 1 | ✅ Docker 환경, DB 모델 완료 |
| M2: 인증 시스템 | Week 2 | JWT 인증, 회원가입/로그인 완료 |
| M3: KIS API 연동 | Week 3 | 계좌 조회, 시장 데이터 수집 완료 |
| M4: 백테스트 엔진 | Week 4 | 백테스트 실행 및 결과 조회 완료 |
| M5: 전략 엔진 | Week 5 | 모멘텀 전략 구현 완료 |
| M6: Frontend 기본 | Week 6 | 인증, 전략 UI 완료 |
| M7: Frontend 완료 | Week 7 | 백테스트 UI, 계좌 UI 완료 |
| M8: 테스트 완료 | Week 8 | 단위, 통합, E2E 테스트 완료 |
| M9: MVP 배포 | Week 9 | 프로덕션 배포 완료 |

---

## 작업 우선순위

### Critical Path (핵심 경로)

```
1. 데이터베이스 구축
   ↓
2. 인증 시스템
   ↓
3. KIS API 연동
   ↓
4. 전략 엔진
   ↓
5. 백테스트 엔진
   ↓
6. Frontend 구현
   ↓
7. 통합 테스트
   ↓
8. 배포
```

### 우선순위별 작업

**P0 (최우선 - Critical)**
- 1.3.1 데이터베이스 구축
- 1.3.2 인증 시스템
- 1.3.3 KIS API 연동
- 1.3.4 전략 엔진
- 1.3.5 백테스트 엔진

**P1 (높음 - High)**
- 1.4.1 인증 UI
- 1.4.2 전략 관리 UI
- 1.4.3 백테스트 UI
- 1.5.2 통합 테스트

**P2 (중간 - Medium)**
- 1.3.6 API 엔드포인트 구현
- 1.4.4 계좌 정보 UI
- 1.5.1 단위 테스트
- 1.6.2 모니터링 설정

**P3 (낮음 - Low)**
- 1.5.3 E2E 테스트
- 1.5.4 성능 테스트
- 문서화

---

## 리소스 및 역할

### 팀 구성

| 역할 | 담당 업무 | 예상 공수 |
|------|----------|----------|
| Backend Developer | API, 데이터베이스, 전략 엔진 | 60시간 |
| Frontend Developer | UI/UX, 컴포넌트 개발 | 36시간 |
| Full Stack Developer | 통합, 테스트, 배포 | 24시간 |

**총 예상 공수:** 120시간

---

## 리스크 관리

### 주요 리스크

| 리스크 | 확률 | 영향 | 완화 방안 |
|--------|------|------|----------|
| KIS API 문서 불명확 | 중간 | 높음 | 사전 API 테스트, 커뮤니티 참고 |
| TA-Lib 설치 문제 | 낮음 | 중간 | Docker 이미지에 사전 설치 |
| 백테스트 성능 저하 | 중간 | 중간 | 데이터 캐싱, 병렬 처리 |
| 데이터베이스 설계 변경 | 낮음 | 높음 | Alembic 마이그레이션 활용 |
| 일정 지연 | 중간 | 중간 | 버퍼 시간 확보, 우선순위 조정 |

### 리스크 대응 전략

1. **KIS API 리스크**
   - API 문서 상세 검토
   - 샘플 코드 작성 및 테스트
   - 에러 케이스 사전 파악

2. **성능 리스크**
   - 초기부터 성능 고려
   - 프로파일링 도구 활용
   - 캐싱 전략 수립

3. **일정 리스크**
   - 주간 진행 상황 점검
   - 블로커 조기 식별
   - 범위 조정 유연성 확보

---

## 품질 기준

### Definition of Done (완료 기준)

**기능 개발:**
- [ ] 코드 작성 완료
- [ ] 단위 테스트 작성 및 통과
- [ ] 코드 리뷰 완료
- [ ] 문서화 완료
- [ ] 통합 테스트 통과

**Phase 완료:**
- [ ] 모든 기능 개발 완료
- [ ] 모든 테스트 통과
- [ ] 주요 버그 수정
- [ ] 문서화 완료
- [ ] 데모 가능

---

## 의존성 관리

### 외부 의존성

| 의존성 | 버전 | 용도 | 대체 방안 |
|--------|------|------|----------|
| FastAPI | 0.109+ | Backend 프레임워크 | Flask, Django |
| Next.js | 14+ | Frontend 프레임워크 | React + Vite |
| PostgreSQL | 15+ | 데이터베이스 | MySQL, MongoDB |
| TA-Lib | 0.4.28 | 기술적 지표 계산 | pandas-ta |
| KIS OpenAPI | - | 증권 API | 다른 증권사 API |

### 내부 의존성

```
인증 시스템 ← 모든 API 엔드포인트
    ↓
KIS API 연동 ← 전략 엔진, 백테스트 엔진
    ↓
전략 엔진 ← 백테스트 엔진
    ↓
Frontend ← Backend API
```

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2025-11-02 | 초기 WBS 작성 | Claude |

---

**문서 끝**

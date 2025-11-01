# 데이터베이스 테이블 명세서

**프로젝트:** Exodus Trading System
**작성일:** 2025-11-02
**버전:** 1.0
**데이터베이스:** PostgreSQL 15+

---

## 목차

1. [users - 사용자](#1-users---사용자)
2. [strategies - 투자 전략](#2-strategies---투자-전략)
3. [signals - 매매 신호](#3-signals---매매-신호)
4. [orders - 주문](#4-orders---주문)
5. [trades - 거래 체결](#5-trades---거래-체결)
6. [holdings - 보유 종목](#6-holdings---보유-종목)
7. [market_data - 시장 데이터](#7-market_data---시장-데이터)
8. [backtest_results - 백테스트 결과](#8-backtest_results---백테스트-결과)
9. [backtest_trades - 백테스트 거래](#9-backtest_trades---백테스트-거래)
10. [관계도](#10-관계도)

---

## 1. users - 사용자

### 설명
사용자 인증 및 프로필 정보를 관리하는 테이블. 한국투자증권 API 인증 정보를 암호화하여 저장.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|--------|------|------|--------|------|
| id | INTEGER | NO | AUTO | 사용자 ID (PK) |
| email | VARCHAR(255) | NO | - | 이메일 주소 (고유) |
| hashed_password | VARCHAR(255) | NO | - | 해시된 비밀번호 (bcrypt) |
| full_name | VARCHAR(100) | NO | - | 사용자 전체 이름 |
| role | ENUM | NO | 'user' | 사용자 역할 (admin, user, viewer) |
| kis_app_key | VARCHAR(255) | YES | NULL | 한국투자증권 APP Key (암호화) |
| kis_app_secret | VARCHAR(255) | YES | NULL | 한국투자증권 APP Secret (암호화) |
| kis_account_number | VARCHAR(50) | YES | NULL | 한국투자증권 계좌번호 |
| kis_account_code | VARCHAR(10) | YES | NULL | 한국투자증권 계좌코드 |
| is_active | BOOLEAN | NO | TRUE | 계정 활성화 상태 |
| is_verified | BOOLEAN | NO | FALSE | 이메일 인증 여부 |
| created_at | TIMESTAMP | NO | NOW() | 생성 일시 |
| updated_at | TIMESTAMP | NO | NOW() | 수정 일시 |

### 인덱스

| 인덱스명 | 타입 | 컬럼 | 설명 |
|----------|------|------|------|
| pk_users | PRIMARY KEY | id | 기본키 |
| idx_users_email | UNIQUE | email | 이메일 고유 인덱스 |

### 제약조건

- **UNIQUE**: email
- **CHECK**: role IN ('admin', 'user', 'viewer')

---

## 2. strategies - 투자 전략

### 설명
사용자가 생성한 투자 전략 정의를 저장. 전략 파라미터는 JSON 형식으로 유연하게 저장.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|--------|------|------|--------|------|
| id | INTEGER | NO | AUTO | 전략 ID (PK) |
| user_id | INTEGER | NO | - | 사용자 ID (FK → users.id) |
| name | VARCHAR(100) | NO | - | 전략 이름 |
| description | VARCHAR(500) | YES | NULL | 전략 설명 |
| strategy_type | ENUM | NO | - | 전략 유형 (momentum, mean_reversion, factor, custom) |
| parameters | JSON | NO | {} | 전략 파라미터 (JSON) |
| is_active | BOOLEAN | NO | FALSE | 전략 활성화 상태 |
| created_at | TIMESTAMP | NO | NOW() | 생성 일시 |
| updated_at | TIMESTAMP | NO | NOW() | 수정 일시 |

### 인덱스

| 인덱스명 | 타입 | 컬럼 | 설명 |
|----------|------|------|------|
| pk_strategies | PRIMARY KEY | id | 기본키 |
| idx_strategies_user_id | INDEX | user_id | 사용자별 전략 조회 |

### 외래키

| 외래키명 | 컬럼 | 참조 테이블 | 참조 컬럼 | ON DELETE |
|----------|------|-------------|----------|-----------|
| fk_strategies_user | user_id | users | id | CASCADE |

### 제약조건

- **CHECK**: strategy_type IN ('momentum', 'mean_reversion', 'factor', 'custom')

### JSON 파라미터 예시

```json
{
  "short_window": 5,
  "long_window": 20,
  "rsi_period": 14,
  "rsi_overbought": 70,
  "rsi_oversold": 30
}
```

---

## 3. signals - 매매 신호

### 설명
전략에 의해 생성된 매매 신호를 기록. 신호의 실행 여부 및 신뢰도를 추적.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|--------|------|------|--------|------|
| id | INTEGER | NO | AUTO | 신호 ID (PK) |
| strategy_id | INTEGER | NO | - | 전략 ID (FK → strategies.id) |
| symbol | VARCHAR(20) | NO | - | 종목 코드 |
| signal_type | ENUM | NO | - | 신호 유형 (buy, sell, hold) |
| confidence | FLOAT | NO | - | 신호 신뢰도 (0.0 ~ 1.0) |
| price | FLOAT | NO | - | 신호 발생 시점 가격 |
| quantity | INTEGER | NO | - | 권장 수량 |
| reason | JSON | NO | {} | 신호 발생 이유 (JSON) |
| is_executed | BOOLEAN | NO | FALSE | 실행 여부 |
| executed_at | TIMESTAMP | YES | NULL | 실행 일시 |
| created_at | TIMESTAMP | NO | NOW() | 생성 일시 |

### 인덱스

| 인덱스명 | 타입 | 컬럼 | 설명 |
|----------|------|------|------|
| pk_signals | PRIMARY KEY | id | 기본키 |
| idx_signals_strategy_id | INDEX | strategy_id | 전략별 신호 조회 |
| idx_signals_symbol | INDEX | symbol | 종목별 신호 조회 |
| idx_signals_created_at | INDEX | created_at | 시간순 조회 |
| idx_signals_strategy_created | INDEX | strategy_id, created_at | 전략별 시간순 조회 |
| idx_signals_symbol_created | INDEX | symbol, created_at | 종목별 시간순 조회 |

### 외래키

| 외래키명 | 컬럼 | 참조 테이블 | 참조 컬럼 | ON DELETE |
|----------|------|-------------|----------|-----------|
| fk_signals_strategy | strategy_id | strategies | id | CASCADE |

### 제약조건

- **CHECK**: signal_type IN ('buy', 'sell', 'hold')
- **CHECK**: confidence >= 0.0 AND confidence <= 1.0
- **CHECK**: price > 0
- **CHECK**: quantity > 0

### JSON Reason 예시

```json
{
  "indicator": "SMA_CROSS",
  "short_ma": 50.5,
  "long_ma": 48.2,
  "volume_spike": true
}
```

---

## 4. orders - 주문

### 설명
주식 주문 실행 및 상태를 관리. 한국투자증권 API를 통한 실제 주문 정보 저장.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|--------|------|------|--------|------|
| id | INTEGER | NO | AUTO | 주문 ID (PK) |
| user_id | INTEGER | NO | - | 사용자 ID (FK → users.id) |
| signal_id | INTEGER | YES | NULL | 신호 ID (FK → signals.id) |
| symbol | VARCHAR(20) | NO | - | 종목 코드 |
| order_type | ENUM | NO | - | 주문 유형 (market, limit, stop) |
| side | ENUM | NO | - | 매수/매도 구분 (buy, sell) |
| quantity | INTEGER | NO | - | 주문 수량 |
| price | FLOAT | YES | NULL | 주문 가격 (시장가의 경우 NULL) |
| status | ENUM | NO | 'pending' | 주문 상태 |
| filled_quantity | INTEGER | NO | 0 | 체결 수량 |
| filled_price | FLOAT | YES | NULL | 체결 가격 |
| commission | FLOAT | NO | 0.0 | 수수료 |
| tax | FLOAT | NO | 0.0 | 세금 |
| external_order_id | VARCHAR(100) | YES | NULL | 외부 주문 ID (KIS API) |
| created_at | TIMESTAMP | NO | NOW() | 주문 생성 일시 |
| submitted_at | TIMESTAMP | YES | NULL | 주문 제출 일시 |
| filled_at | TIMESTAMP | YES | NULL | 체결 완료 일시 |
| updated_at | TIMESTAMP | NO | NOW() | 수정 일시 |

### 인덱스

| 인덱스명 | 타입 | 컬럼 | 설명 |
|----------|------|------|------|
| pk_orders | PRIMARY KEY | id | 기본키 |
| idx_orders_user_id | INDEX | user_id | 사용자별 주문 조회 |
| idx_orders_signal_id | INDEX | signal_id | 신호별 주문 조회 |
| idx_orders_symbol | INDEX | symbol | 종목별 주문 조회 |
| idx_orders_status | INDEX | status | 상태별 주문 조회 |
| idx_orders_external_order_id | INDEX | external_order_id | 외부 주문 ID 조회 |
| idx_orders_created_at | INDEX | created_at | 시간순 조회 |
| idx_orders_user_created | INDEX | user_id, created_at | 사용자별 시간순 조회 |
| idx_orders_symbol_created | INDEX | symbol, created_at | 종목별 시간순 조회 |
| idx_orders_status_created | INDEX | status, created_at | 상태별 시간순 조회 |

### 외래키

| 외래키명 | 컬럼 | 참조 테이블 | 참조 컬럼 | ON DELETE |
|----------|------|-------------|----------|-----------|
| fk_orders_user | user_id | users | id | CASCADE |
| fk_orders_signal | signal_id | signals | id | SET NULL |

### 제약조건

- **CHECK**: order_type IN ('market', 'limit', 'stop')
- **CHECK**: side IN ('buy', 'sell')
- **CHECK**: status IN ('pending', 'submitted', 'filled', 'partially_filled', 'cancelled', 'rejected')
- **CHECK**: quantity > 0
- **CHECK**: filled_quantity >= 0
- **CHECK**: filled_quantity <= quantity

---

## 5. trades - 거래 체결

### 설명
실제로 체결된 거래 내역을 기록. 수수료 및 세금을 포함한 실거래 금액 저장.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|--------|------|------|--------|------|
| id | INTEGER | NO | AUTO | 거래 ID (PK) |
| order_id | INTEGER | NO | - | 주문 ID (FK → orders.id) |
| user_id | INTEGER | NO | - | 사용자 ID (FK → users.id) |
| symbol | VARCHAR(20) | NO | - | 종목 코드 |
| side | ENUM | NO | - | 매수/매도 구분 (buy, sell) |
| quantity | INTEGER | NO | - | 체결 수량 |
| price | FLOAT | NO | - | 체결 가격 |
| commission | FLOAT | NO | 0.0 | 수수료 |
| tax | FLOAT | NO | 0.0 | 세금 (매도시 증권거래세) |
| total_amount | FLOAT | NO | - | 총 거래 금액 |
| executed_at | TIMESTAMP | NO | NOW() | 체결 일시 |
| created_at | TIMESTAMP | NO | NOW() | 생성 일시 |

### 인덱스

| 인덱스명 | 타입 | 컬럼 | 설명 |
|----------|------|------|------|
| pk_trades | PRIMARY KEY | id | 기본키 |
| idx_trades_order_id | INDEX | order_id | 주문별 거래 조회 |
| idx_trades_user_id | INDEX | user_id | 사용자별 거래 조회 |
| idx_trades_symbol | INDEX | symbol | 종목별 거래 조회 |
| idx_trades_executed_at | INDEX | executed_at | 체결 시간순 조회 |
| idx_trades_user_executed | INDEX | user_id, executed_at | 사용자별 시간순 조회 |
| idx_trades_symbol_executed | INDEX | symbol, executed_at | 종목별 시간순 조회 |

### 외래키

| 외래키명 | 컬럼 | 참조 테이블 | 참조 컬럼 | ON DELETE |
|----------|------|-------------|----------|-----------|
| fk_trades_order | order_id | orders | id | CASCADE |
| fk_trades_user | user_id | users | id | CASCADE |

### 제약조건

- **CHECK**: side IN ('buy', 'sell')
- **CHECK**: quantity > 0
- **CHECK**: price > 0
- **CHECK**: total_amount > 0

### 총 거래 금액 계산

- **매수**: `total_amount = (quantity * price) + commission + tax`
- **매도**: `total_amount = (quantity * price) - commission - tax`

---

## 6. holdings - 보유 종목

### 설명
사용자의 현재 보유 종목 및 평가 손익을 관리. 실시간으로 업데이트되는 포트폴리오 정보.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|--------|------|------|--------|------|
| id | INTEGER | NO | AUTO | 보유 ID (PK) |
| user_id | INTEGER | NO | - | 사용자 ID (FK → users.id) |
| symbol | VARCHAR(20) | NO | - | 종목 코드 |
| company_name | VARCHAR(100) | YES | NULL | 회사명 |
| quantity | INTEGER | NO | - | 보유 수량 |
| average_price | FLOAT | NO | - | 평균 매입 단가 |
| current_price | FLOAT | NO | - | 현재가 |
| total_cost | FLOAT | NO | - | 총 매입 금액 |
| current_value | FLOAT | NO | - | 현재 평가 금액 |
| unrealized_pnl | FLOAT | NO | - | 미실현 손익 (금액) |
| unrealized_pnl_percent | FLOAT | NO | - | 미실현 손익률 (%) |
| updated_at | TIMESTAMP | NO | NOW() | 수정 일시 |
| created_at | TIMESTAMP | NO | NOW() | 생성 일시 |

### 인덱스

| 인덱스명 | 타입 | 컬럼 | 설명 |
|----------|------|------|------|
| pk_holdings | PRIMARY KEY | id | 기본키 |
| idx_holdings_user_id | INDEX | user_id | 사용자별 보유 종목 조회 |
| idx_holdings_symbol | INDEX | symbol | 종목별 조회 |
| idx_holdings_updated_at | INDEX | updated_at | 업데이트 시간순 조회 |
| idx_holdings_user_symbol | UNIQUE | user_id, symbol | 사용자별 종목 고유 |

### 외래키

| 외래키명 | 컬럼 | 참조 테이블 | 참조 컬럼 | ON DELETE |
|----------|------|-------------|----------|-----------|
| fk_holdings_user | user_id | users | id | CASCADE |

### 제약조건

- **UNIQUE**: (user_id, symbol) - 사용자당 종목별 하나의 레코드만 존재
- **CHECK**: quantity > 0
- **CHECK**: average_price > 0
- **CHECK**: current_price > 0

### 계산 공식

```
total_cost = quantity * average_price
current_value = quantity * current_price
unrealized_pnl = current_value - total_cost
unrealized_pnl_percent = (unrealized_pnl / total_cost) * 100
```

---

## 7. market_data - 시장 데이터

### 설명
OHLCV (Open, High, Low, Close, Volume) 시계열 데이터 저장. 다양한 시간 간격 지원.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|--------|------|------|--------|------|
| id | INTEGER | NO | AUTO | 데이터 ID (PK) |
| symbol | VARCHAR(20) | NO | - | 종목 코드 |
| timestamp | TIMESTAMP | NO | - | 데이터 시점 |
| open | FLOAT | NO | - | 시가 |
| high | FLOAT | NO | - | 고가 |
| low | FLOAT | NO | - | 저가 |
| close | FLOAT | NO | - | 종가 |
| volume | FLOAT | NO | - | 거래량 |
| interval | ENUM | NO | - | 시간 간격 (1m, 5m, 10m, 30m, 1h, 1d) |
| created_at | TIMESTAMP | NO | NOW() | 생성 일시 |

### 인덱스

| 인덱스명 | 타입 | 컬럼 | 설명 |
|----------|------|------|------|
| pk_market_data | PRIMARY KEY | id | 기본키 |
| idx_market_data_symbol | INDEX | symbol | 종목별 조회 |
| idx_market_data_timestamp | INDEX | timestamp | 시간순 조회 |
| idx_market_data_interval | INDEX | interval | 간격별 조회 |
| idx_market_data_symbol_timestamp | INDEX | symbol, timestamp | 종목별 시간순 조회 |
| idx_market_data_symbol_interval_timestamp | INDEX | symbol, interval, timestamp | 종목/간격별 시간순 조회 |
| idx_market_data_unique | UNIQUE | symbol, timestamp, interval | 중복 방지 |

### 제약조건

- **UNIQUE**: (symbol, timestamp, interval) - 중복 데이터 방지
- **CHECK**: interval IN ('1m', '5m', '10m', '30m', '1h', '1d')
- **CHECK**: open > 0
- **CHECK**: high > 0
- **CHECK**: low > 0
- **CHECK**: close > 0
- **CHECK**: volume >= 0
- **CHECK**: high >= low
- **CHECK**: high >= open
- **CHECK**: high >= close
- **CHECK**: low <= open
- **CHECK**: low <= close

---

## 8. backtest_results - 백테스트 결과

### 설명
전략 백테스트 실행 결과 및 성과 지표를 저장. 상세한 분석 데이터는 JSON 형태로 저장.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|--------|------|------|--------|------|
| id | INTEGER | NO | AUTO | 백테스트 ID (PK) |
| strategy_id | INTEGER | NO | - | 전략 ID (FK → strategies.id) |
| user_id | INTEGER | NO | - | 사용자 ID (FK → users.id) |
| name | VARCHAR(100) | NO | - | 백테스트 이름 |
| start_date | DATE | NO | - | 백테스트 시작일 |
| end_date | DATE | NO | - | 백테스트 종료일 |
| initial_capital | FLOAT | NO | - | 초기 자본금 |
| final_capital | FLOAT | NO | - | 최종 자본금 |
| total_return | FLOAT | NO | - | 총 수익률 (%) |
| annual_return | FLOAT | NO | - | 연환산 수익률 (%) |
| max_drawdown | FLOAT | NO | - | 최대 낙폭 (%) |
| sharpe_ratio | FLOAT | NO | - | 샤프 지수 |
| total_trades | INTEGER | NO | - | 총 거래 횟수 |
| winning_trades | INTEGER | NO | - | 수익 거래 횟수 |
| losing_trades | INTEGER | NO | - | 손실 거래 횟수 |
| win_rate | FLOAT | NO | - | 승률 (%) |
| average_win | FLOAT | NO | - | 평균 수익 금액 |
| average_loss | FLOAT | NO | - | 평균 손실 금액 |
| profit_loss_ratio | FLOAT | NO | - | 손익비 |
| largest_win | FLOAT | NO | - | 최대 수익 금액 |
| largest_loss | FLOAT | NO | - | 최대 손실 금액 |
| average_holding_period | FLOAT | NO | - | 평균 보유 기간 (일) |
| results_detail | JSON | NO | {} | 상세 결과 (JSON) |
| created_at | TIMESTAMP | NO | NOW() | 생성 일시 |

### 인덱스

| 인덱스명 | 타입 | 컬럼 | 설명 |
|----------|------|------|------|
| pk_backtest_results | PRIMARY KEY | id | 기본키 |
| idx_backtest_results_strategy_id | INDEX | strategy_id | 전략별 백테스트 조회 |
| idx_backtest_results_user_id | INDEX | user_id | 사용자별 백테스트 조회 |
| idx_backtest_results_created_at | INDEX | created_at | 시간순 조회 |
| idx_backtest_results_user_created | INDEX | user_id, created_at | 사용자별 시간순 조회 |
| idx_backtest_results_strategy_created | INDEX | strategy_id, created_at | 전략별 시간순 조회 |

### 외래키

| 외래키명 | 컬럼 | 참조 테이블 | 참조 컬럼 | ON DELETE |
|----------|------|-------------|----------|-----------|
| fk_backtest_results_strategy | strategy_id | strategies | id | CASCADE |
| fk_backtest_results_user | user_id | users | id | CASCADE |

### 제약조건

- **CHECK**: initial_capital > 0
- **CHECK**: final_capital >= 0
- **CHECK**: total_trades >= 0
- **CHECK**: winning_trades >= 0
- **CHECK**: losing_trades >= 0
- **CHECK**: win_rate >= 0 AND win_rate <= 100
- **CHECK**: end_date >= start_date

### JSON results_detail 예시

```json
{
  "daily_returns": [0.01, -0.005, 0.02, ...],
  "equity_curve": [100000, 101000, 100500, 102500, ...],
  "drawdown_curve": [0, -0.5, -1.2, 0, ...],
  "monthly_returns": {
    "2024-01": 5.2,
    "2024-02": -2.1,
    "2024-03": 8.5
  }
}
```

---

## 9. backtest_trades - 백테스트 거래

### 설명
백테스트 실행 중 발생한 개별 거래 내역을 저장. 각 거래의 신호 발생 이유 포함.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|--------|------|------|--------|------|
| id | INTEGER | NO | AUTO | 거래 ID (PK) |
| backtest_id | INTEGER | NO | - | 백테스트 ID (FK → backtest_results.id) |
| symbol | VARCHAR(20) | NO | - | 종목 코드 |
| side | VARCHAR(10) | NO | - | 매수/매도 구분 (buy, sell) |
| quantity | INTEGER | NO | - | 거래 수량 |
| price | FLOAT | NO | - | 거래 가격 |
| commission | FLOAT | NO | 0.0 | 수수료 |
| trade_date | DATE | NO | - | 거래 일자 |
| signal_reason | JSON | NO | {} | 신호 발생 이유 (JSON) |
| created_at | TIMESTAMP | NO | NOW() | 생성 일시 |

### 인덱스

| 인덱스명 | 타입 | 컬럼 | 설명 |
|----------|------|------|------|
| pk_backtest_trades | PRIMARY KEY | id | 기본키 |
| idx_backtest_trades_backtest_id | INDEX | backtest_id | 백테스트별 거래 조회 |
| idx_backtest_trades_symbol | INDEX | symbol | 종목별 거래 조회 |
| idx_backtest_trades_trade_date | INDEX | trade_date | 거래일별 조회 |
| idx_backtest_trades_backtest_date | INDEX | backtest_id, trade_date | 백테스트별 일자순 조회 |

### 외래키

| 외래키명 | 컬럼 | 참조 테이블 | 참조 컬럼 | ON DELETE |
|----------|------|-------------|----------|-----------|
| fk_backtest_trades_backtest | backtest_id | backtest_results | id | CASCADE |

### 제약조건

- **CHECK**: side IN ('buy', 'sell')
- **CHECK**: quantity > 0
- **CHECK**: price > 0
- **CHECK**: commission >= 0

---

## 10. 관계도

### ERD (Entity Relationship Diagram)

```
┌─────────────────┐
│     users       │
│─────────────────│
│ id (PK)         │
│ email           │
│ hashed_password │
│ full_name       │
│ role            │
│ kis_*           │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────┴────┬────────┬──────────┬─────────────┐
    │         │        │          │             │
    ▼         ▼        ▼          ▼             ▼
┌─────────┐ ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────────┐
│strategies│ │ orders │ │ trades │ │ holdings │ │backtest_     │
│         │ │        │ │        │ │          │ │results       │
└────┬────┘ └───┬────┘ └────────┘ └──────────┘ └──────┬───────┘
     │          │                                      │
     │ 1:N      │ N:1                                  │ 1:N
     │          │                                      │
     ▼          ▼                                      ▼
┌─────────┐ ┌─────────┐                         ┌──────────────┐
│ signals │ │         │                         │backtest_     │
│         │◄┘         │                         │trades        │
└─────────┘           │                         └──────────────┘
                      │
                      │ 1:N
                      │
                      ▼
                 ┌─────────┐
                 │ trades  │
                 │         │
                 └─────────┘

┌──────────────┐
│ market_data  │  (독립적인 시계열 데이터)
│              │
└──────────────┘
```

### 관계 요약

| 부모 테이블 | 자식 테이블 | 관계 | 외래키 | ON DELETE |
|------------|------------|------|--------|-----------|
| users | strategies | 1:N | strategies.user_id | CASCADE |
| users | orders | 1:N | orders.user_id | CASCADE |
| users | trades | 1:N | trades.user_id | CASCADE |
| users | holdings | 1:N | holdings.user_id | CASCADE |
| users | backtest_results | 1:N | backtest_results.user_id | CASCADE |
| strategies | signals | 1:N | signals.strategy_id | CASCADE |
| strategies | backtest_results | 1:N | backtest_results.strategy_id | CASCADE |
| signals | orders | 1:N | orders.signal_id | SET NULL |
| orders | trades | 1:N | trades.order_id | CASCADE |
| backtest_results | backtest_trades | 1:N | backtest_trades.backtest_id | CASCADE |

### Cascade 동작

- **CASCADE**: 부모 레코드 삭제 시 자식 레코드도 함께 삭제
- **SET NULL**: 부모 레코드 삭제 시 자식의 외래키를 NULL로 설정

---

## 11. 인덱싱 전략

### 주요 조회 패턴별 인덱스

1. **사용자별 데이터 조회**
   - `idx_strategies_user_id`
   - `idx_orders_user_id`
   - `idx_trades_user_id`
   - `idx_holdings_user_id`

2. **시간순 조회**
   - `idx_signals_created_at`
   - `idx_orders_created_at`
   - `idx_trades_executed_at`
   - `idx_backtest_results_created_at`

3. **복합 조회 (사용자 + 시간)**
   - `idx_orders_user_created`
   - `idx_trades_user_executed`
   - `idx_backtest_results_user_created`

4. **종목별 조회**
   - `idx_signals_symbol`
   - `idx_orders_symbol`
   - `idx_trades_symbol`
   - `idx_market_data_symbol_timestamp`

5. **고유성 보장**
   - `idx_users_email` (UNIQUE)
   - `idx_holdings_user_symbol` (UNIQUE)
   - `idx_market_data_unique` (UNIQUE)

---

## 12. 데이터 타입 및 제약

### Enum 타입

| Enum 이름 | 값 | 사용 테이블 |
|-----------|-------|------------|
| user_role | admin, user, viewer | users |
| strategy_type | momentum, mean_reversion, factor, custom | strategies |
| signal_type | buy, sell, hold | signals |
| order_type | market, limit, stop | orders |
| order_side | buy, sell | orders, trades |
| order_status | pending, submitted, filled, partially_filled, cancelled, rejected | orders |
| time_interval | 1m, 5m, 10m, 30m, 1h, 1d | market_data |

### JSON 필드 활용

| 테이블 | 컬럼 | 용도 |
|-------|------|------|
| strategies | parameters | 전략 파라미터 (이동평균 기간, RSI 임계값 등) |
| signals | reason | 신호 발생 이유 (지표 값, 조건 등) |
| backtest_results | results_detail | 상세 성과 데이터 (일별 수익률, 자본 곡선 등) |
| backtest_trades | signal_reason | 백테스트 거래 발생 이유 |

---

## 13. 데이터베이스 크기 예측

### 예상 레코드 수 (연간)

| 테이블 | 예상 레코드 수 | 예상 크기 |
|-------|--------------|----------|
| users | 1,000 | ~100 KB |
| strategies | 5,000 | ~500 KB |
| signals | 500,000 | ~50 MB |
| orders | 100,000 | ~15 MB |
| trades | 100,000 | ~10 MB |
| holdings | 10,000 | ~1 MB |
| market_data (1d) | 500,000 | ~50 MB |
| market_data (1m) | 72,000,000 | ~7 GB |
| backtest_results | 10,000 | ~5 MB |
| backtest_trades | 1,000,000 | ~100 MB |

**총 예상 크기 (1년)**: ~7.3 GB (1분봉 포함)

### 최적화 고려사항

1. **파티셔닝**: market_data 테이블을 날짜별로 파티셔닝
2. **아카이빙**: 오래된 백테스트 결과 아카이빙
3. **인덱스 유지보수**: VACUUM, ANALYZE 정기 실행
4. **데이터 압축**: TimescaleDB 사용 시 자동 압축

---

## 14. 마이그레이션 가이드

### Alembic 마이그레이션 생성

```bash
# 초기 마이그레이션 생성
cd backend
alembic revision --autogenerate -m "Initial database schema"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

### 데이터베이스 생성

```sql
CREATE DATABASE exodus_trading
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;
```

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2025-11-02 | 초기 테이블 명세서 작성 | Claude |

---

**문서 끝**

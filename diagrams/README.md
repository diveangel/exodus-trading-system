# Exodus Trading System - Architecture Diagrams

이 디렉토리는 Exodus Trading System의 아키텍처를 시각화한 PlantUML 다이어그램을 포함하고 있습니다.

## 📁 다이어그램 목록

### 1. System Context Diagram (01-system-context.puml)
**목적**: 시스템의 전체적인 컨텍스트와 외부 시스템과의 상호작용 표시

**내용**:
- 주요 액터: 투자자, 관리자
- 외부 시스템: 한국투자증권 OpenAPI, 이메일 서비스
- 시스템 경계 및 통신 방식

### 2. Container Diagram (02-container.puml)
**목적**: 시스템을 구성하는 주요 컨테이너(애플리케이션)와 그들 간의 관계 표시

**내용**:
- Frontend (Next.js)
- Backend API (FastAPI)
- Background Worker (Celery)
- PostgreSQL Database
- Redis Cache
- Nginx Reverse Proxy
- 컨테이너 간 통신 프로토콜

### 3. Component Diagram - Backend (03-component-backend.puml)
**목적**: Backend API 서버의 내부 컴포넌트 구조 상세 표시

**내용**:
- API Layer: Auth, Account, Strategy, Backtest, Order, Market API
- Core Layer: Strategy Manager, Signal Generator, Order Executor, Risk Manager, Backtest Engine
- Service Layer: User, Account, Market Data, KIS API, Notification Service
- 컴포넌트 간 의존성 및 데이터 흐름

### 4. Sequence Diagram - User Login (04-sequence-login.puml)
**목적**: 사용자 로그인 프로세스의 순차적 흐름 표시

**주요 단계**:
1. 사용자가 로그인 페이지 접속
2. 이메일/비밀번호 입력 및 전송
3. Backend에서 사용자 검증
4. JWT 토큰 (Access + Refresh) 생성
5. Redis에 Refresh Token 저장
6. 토큰을 Frontend로 반환
7. Frontend에서 토큰 저장 및 대시보드로 리디렉션

### 5. Sequence Diagram - Auto Trading (05-sequence-auto-trading.puml)
**목적**: 자동매매 실행의 전체 플로우 표시

**주요 단계**:
1. Scheduler가 주기적으로 전략 실행 트리거
2. Strategy Manager가 활성화된 전략 조회
3. Signal Generator가 매매 신호 생성
4. Risk Manager가 리스크 검증
5. Order Executor가 주문 실행
6. 한국투자증권 API를 통해 주문 전송
7. WebSocket을 통한 실시간 알림
8. 별도 프로세스에서 체결 확인 및 처리

### 6. Sequence Diagram - Backtest (06-sequence-backtest.puml)
**목적**: 백테스트 실행 및 결과 조회 프로세스 표시

**주요 단계**:
1. 사용자가 백테스트 설정 (전략, 기간, 초기 자금)
2. Backend가 백테스트 Task를 Background Worker에 등록
3. Worker가 과거 시장 데이터 조회
4. 날짜별로 전략을 시뮬레이션하며 가상 주문 실행
5. 최종 성과 지표 계산 (수익률, MDD, Sharpe Ratio 등)
6. 결과를 Database에 저장
7. WebSocket을 통해 완료 알림
8. 사용자가 결과 페이지에서 시각화된 결과 확인

### 7. Database ER Diagram (07-database-er.puml)
**목적**: 데이터베이스 스키마 및 테이블 간 관계 표시

**주요 테이블**:
- **users**: 사용자 정보 및 인증
- **strategies**: 투자 전략 정의
- **signals**: 매매 신호 기록
- **orders**: 주문 내역
- **trades**: 체결 내역
- **holdings**: 보유 종목
- **market_data**: 시장 데이터 (시계열)
- **backtest_results**: 백테스트 결과
- **backtest_trades**: 백테스트 거래 기록
- **account_snapshots**: 일일 계좌 스냅샷
- **notifications**: 알림

**관계**:
- 1:N 관계: users ↔ strategies, users ↔ orders, strategies ↔ signals 등
- Cascade 삭제 및 외래 키 제약 조건

### 8. Deployment Diagram (08-deployment.puml)
**목적**: Docker Compose 기반 배포 아키텍처 표시

**내용**:
- Docker Host 및 Docker Network 구성
- 6개 주요 컨테이너: nginx, frontend, backend, worker, postgres, redis
- Docker Volumes를 통한 데이터 영속성
- 컨테이너 간 네트워크 통신
- 포트 매핑 및 외부 접근

---

## 🔧 다이어그램 렌더링 방법

### 1. PlantUML 온라인 에디터
- [PlantUML Online Editor](http://www.plantuml.com/plantuml/uml/)
- `.puml` 파일 내용을 복사하여 붙여넣기

### 2. VS Code 확장
```bash
# PlantUML 확장 설치
VS Code Extensions > 검색: "PlantUML"
```

**사용법**:
1. `.puml` 파일 열기
2. `Alt + D` (미리보기)
3. `Ctrl + Shift + P` > "PlantUML: Export Current Diagram"

### 3. CLI 도구 (Java 필요)
```bash
# PlantUML JAR 다운로드
wget https://sourceforge.net/projects/plantuml/files/plantuml.jar/download -O plantuml.jar

# 다이어그램 생성 (PNG)
java -jar plantuml.jar diagrams/*.puml

# 다이어그램 생성 (SVG)
java -jar plantuml.jar -tsvg diagrams/*.puml
```

### 4. Docker를 사용한 렌더링
```bash
# PlantUML Docker 컨테이너 실행
docker run -d -p 8080:8080 plantuml/plantuml-server:jetty

# 브라우저에서 http://localhost:8080 접속
# .puml 파일 내용을 붙여넣기
```

---

## 📊 다이어그램 출력 예시

생성된 다이어그램은 다음과 같은 형식으로 저장할 수 있습니다:
- **PNG**: 문서 및 프레젠테이션용
- **SVG**: 웹 및 확대/축소가 필요한 경우
- **PDF**: 인쇄용

```bash
# 모든 다이어그램을 PNG로 변환
java -jar plantuml.jar -tpng diagrams/*.puml

# 출력 디렉토리 지정
java -jar plantuml.jar -tpng -o ../images diagrams/*.puml
```

---

## 🎨 다이어그램 스타일 가이드

### C4 Model
- System Context, Container, Component 다이어그램은 [C4 Model](https://c4model.com/) 표준을 따릅니다.
- C4-PlantUML 라이브러리 사용

### ER Diagram
- PlantUML Entity-Relationship 구문 사용
- Primary Key (PK), Foreign Key (FK), Unique (UQ) 표시

### Sequence Diagram
- 시간 순서에 따른 상호작용 표시
- activate/deactivate로 생명주기 표시
- alt/else로 조건 분기 표시
- loop로 반복 처리 표시

---

## 📝 다이어그램 업데이트

다이어그램을 수정하려면:

1. 해당 `.puml` 파일 편집
2. 렌더링하여 결과 확인
3. Git에 커밋

```bash
# 다이어그램 파일 수정
vi diagrams/02-container.puml

# 렌더링 테스트
java -jar plantuml.jar diagrams/02-container.puml

# Git 커밋
git add diagrams/02-container.puml
git commit -m "Update: Container diagram with new service"
```

---

## 🔗 참고 자료

- [PlantUML 공식 문서](https://plantuml.com/)
- [C4 Model](https://c4model.com/)
- [C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML)
- [PlantUML Cheat Sheet](https://plantuml.com/guide)

---

**문서 버전**: 1.0
**최종 업데이트**: 2025-10-28

# Server Management Scripts

Exodus Trading System의 백엔드와 프론트엔드 서버를 쉽게 관리할 수 있는 스크립트입니다.

## 📋 목차

- [스크립트 개요](#스크립트-개요)
- [사전 준비](#사전-준비)
- [사용 방법](#사용-방법)
- [로그 확인](#로그-확인)
- [문제 해결](#문제-해결)

## 📦 스크립트 개요

### 1. restart-servers.sh
백엔드와 프론트엔드 서버를 재시작하는 스크립트입니다.

**수행 작업:**
1. 실행 중인 백엔드 서버 체크 및 종료 (포트 8000)
2. 실행 중인 프론트엔드 서버 체크 및 종료 (포트 3000, 3001)
3. 백엔드 서버 시작
4. 프론트엔드 서버 시작

### 2. stop-servers.sh
실행 중인 모든 서버를 종료하는 스크립트입니다.

**수행 작업:**
1. 백엔드 서버 종료 (포트 8000)
2. 프론트엔드 서버 종료 (포트 3000, 3001)

## 🔧 사전 준비

### 1. 스크립트에 실행 권한 부여

```bash
chmod +x restart-servers.sh stop-servers.sh
```

### 2. 필요한 의존성 설치 확인

**백엔드:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**프론트엔드:**
```bash
cd frontend
npm install
```

## 🚀 사용 방법

### 서버 재시작

프로젝트 루트 디렉토리에서 실행:

```bash
./restart-servers.sh
```

**실행 결과 예시:**
```
========================================
  Exodus Trading System Server Manager
========================================

[1/4] Stopping Backend Server...
✓ Port 8000 is now free

[2/4] Stopping Frontend Server...
✓ Port 3000 is now free
✓ Port 3001 is now free

[3/4] Starting Backend Server...
✓ Backend server started successfully (PID: 12345)
  URL: http://localhost:8000
  Docs: http://localhost:8000/docs
  Logs: /path/to/backend/backend.log

[4/4] Starting Frontend Server...
✓ Frontend server started successfully (PID: 12346)
  URL: http://localhost:3001
  Logs: /path/to/frontend/frontend.log

========================================
  ✓ All servers started successfully!
========================================

Backend:  http://localhost:8000
Frontend: http://localhost:3001
API Docs: http://localhost:8000/docs
```

### 서버 중지

프로젝트 루트 디렉토리에서 실행:

```bash
./stop-servers.sh
```

**실행 결과 예시:**
```
========================================
  Stopping Exodus Trading System
========================================

[1/2] Stopping Backend Server...
✓ Stopped backend

[2/2] Stopping Frontend Server...
✓ Stopped frontend

========================================
  ✓ All servers stopped successfully!
========================================
```

## 📊 로그 확인

### 백엔드 로그 보기

```bash
# 실시간 로그 확인
tail -f backend/backend.log

# 최근 100줄 보기
tail -n 100 backend/backend.log

# 전체 로그 보기
cat backend/backend.log
```

### 프론트엔드 로그 보기

```bash
# 실시간 로그 확인
tail -f frontend/frontend.log

# 최근 100줄 보기
tail -n 100 frontend/frontend.log

# 전체 로그 보기
cat frontend/frontend.log
```

### 특정 에러 찾기

```bash
# 백엔드 에러 로그
grep -i error backend/backend.log

# 프론트엔드 에러 로그
grep -i error frontend/frontend.log

# KIS API 관련 로그
grep -i "kis" backend/backend.log
```

## 🔍 문제 해결

### 1. 스크립트 실행 권한 오류

**문제:**
```
bash: ./restart-servers.sh: Permission denied
```

**해결:**
```bash
chmod +x restart-servers.sh stop-servers.sh
```

### 2. 포트가 이미 사용 중

**문제:**
```
✗ Failed to free port 8000
```

**해결:**
```bash
# 포트 사용 중인 프로세스 확인
lsof -ti:8000

# 프로세스 강제 종료
kill -9 $(lsof -ti:8000)

# 또는 stop-servers.sh 실행 후 재시도
./stop-servers.sh
./restart-servers.sh
```

### 3. 백엔드 서버 시작 실패

**문제:**
```
✗ Failed to start backend server
```

**해결 방법:**

1. **가상환경 확인:**
```bash
cd backend
ls -la venv/  # venv 디렉토리가 있는지 확인
```

2. **의존성 재설치:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

3. **데이터베이스 연결 확인:**
```bash
# PostgreSQL 컨테이너 실행 확인
docker ps | grep exodus-postgres

# 컨테이너 시작
docker start exodus-postgres
```

4. **로그 확인:**
```bash
tail -f backend/backend.log
```

### 4. 프론트엔드 서버 시작 실패

**문제:**
```
✗ Failed to start frontend server
```

**해결 방법:**

1. **node_modules 확인:**
```bash
cd frontend
ls -la node_modules/  # node_modules 디렉토리가 있는지 확인
```

2. **의존성 재설치:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

3. **캐시 삭제:**
```bash
cd frontend
rm -rf .next
```

4. **로그 확인:**
```bash
tail -f frontend/frontend.log
```

### 5. Python 가상환경이 없음

**문제:**
```
✗ Virtual environment not found!
```

**해결:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6. Node modules가 없음

**문제:**
```
✗ node_modules not found!
```

**해결:**
```bash
cd frontend
npm install
```

## 📝 추가 명령어

### 수동으로 서버 시작

**백엔드:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**프론트엔드:**
```bash
cd frontend
npm run dev
```

### 프로세스 ID(PID) 확인

**PID 파일 위치:**
- 백엔드: `backend/.backend.pid`
- 프론트엔드: `frontend/.frontend.pid`

**PID 확인:**
```bash
# 백엔드 PID
cat backend/.backend.pid

# 프론트엔드 PID
cat frontend/.frontend.pid
```

### 특정 포트의 프로세스 확인

```bash
# 포트 8000 (백엔드)
lsof -ti:8000

# 포트 3001 (프론트엔드)
lsof -ti:3001

# 자세한 정보 보기
lsof -i:8000
```

## 🌐 접속 URL

서버 시작 후 브라우저에서 아래 URL로 접속:

- **프론트엔드**: http://localhost:3001
- **백엔드 API**: http://localhost:8000
- **API 문서 (Swagger)**: http://localhost:8000/docs
- **API 문서 (ReDoc)**: http://localhost:8000/redoc

## ⚙️ 환경 변수

스크립트는 다음 환경 변수를 자동으로 사용합니다:

**백엔드 (.env 파일):**
- DATABASE_URL
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES

**프론트엔드 (.env.local 파일):**
- NEXT_PUBLIC_API_URL

환경 변수 파일이 없으면 기본값이 사용됩니다.

## 💡 팁

1. **개발 중 자동 재시작**:
   - 백엔드: `--reload` 옵션으로 코드 변경 시 자동 재시작
   - 프론트엔드: Next.js가 자동으로 Hot Reload 지원

2. **로그 모니터링**:
   ```bash
   # 두 개의 터미널을 열어서 동시에 모니터링
   # 터미널 1
   tail -f backend/backend.log

   # 터미널 2
   tail -f frontend/frontend.log
   ```

3. **빠른 재시작**:
   코드 변경 후 빠르게 재시작하려면:
   ```bash
   ./restart-servers.sh
   ```

4. **깔끔한 종료**:
   작업 종료 시:
   ```bash
   ./stop-servers.sh
   ```

## 🐛 버그 리포트

문제가 발생하면 다음 정보와 함께 이슈를 생성해주세요:

1. 실행한 명령어
2. 에러 메시지
3. 백엔드/프론트엔드 로그 파일 내용
4. 운영체제 정보

---

**Last Updated:** 2025-11-03
**Version:** 1.0.0

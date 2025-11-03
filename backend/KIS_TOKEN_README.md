# KIS API Token Management

KIS API 인증 토큰을 로컬 파일로 저장하고 관리하는 시스템입니다.

## 📋 개요

### 주요 기능

1. **토큰 파일 저장**: 발급받은 액세스 토큰을 로컬 파일에 저장
2. **자동 토큰 재사용**: 유효한 토큰이 있으면 파일에서 로드하여 재사용
3. **토큰 만료 감지**: 토큰 유효기간을 자동으로 판단
4. **자동 재발급**: 만료된 토큰은 자동으로 재발급

## 🏗️ 구조

### 1. KISTokenManager (`app/services/kis_token_manager.py`)

토큰의 저장, 로드, 삭제를 담당하는 관리자 클래스입니다.

**주요 메서드:**
- `save_token(token)`: 토큰을 파일로 저장
- `load_token()`: 파일에서 토큰 로드 (만료 체크 포함)
- `delete_token()`: 토큰 파일 삭제
- `get_token_info()`: 토큰 메타데이터 조회

**토큰 파일 위치:**
```
~/KIS/tokens/token_{app_key_prefix}_{mode}.json
```

예시:
- `~/KIS/tokens/token_PStoMm5NMd_mock.json` (모의투자)
- `~/KIS/tokens/token_PStoMm5NMd_real.json` (실전투자)

### 2. KISToken (`app/services/kis_token_manager.py`)

토큰 데이터를 담는 모델 클래스입니다.

**필드:**
- `access_token`: 액세스 토큰 문자열
- `token_type`: 토큰 타입 (일반적으로 "Bearer")
- `expires_in`: 유효 기간 (초)
- `issued_at`: 발급 시각

**메서드:**
- `is_expired(buffer_seconds)`: 토큰 만료 여부 확인 (기본 5분 버퍼)
- `get_expiry_datetime()`: 정확한 만료 시각 반환

### 3. KISClient (`app/services/kis_client.py`)

KIS API 클라이언트로, 토큰 관리자를 사용하여 인증을 처리합니다.

**토큰 확보 흐름 (`_ensure_token`):**

```
1. 메모리에 토큰이 있고 유효한가?
   ├─ Yes → 메모리 토큰 사용
   └─ No → 다음 단계

2. 파일에 토큰이 있고 유효한가?
   ├─ Yes → 파일에서 로드하여 사용
   └─ No → 다음 단계

3. KIS API에 새 토큰 요청
   └─ 성공 → 파일에 저장 후 사용
```

## 📁 파일 구조

```
~/KIS/
└── tokens/
    ├── token_PStoMm5NMd_mock.json
    └── token_PStoMm5NMd_real.json
```

**토큰 파일 형식:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "issued_at": "2025-11-03T19:45:30.123456",
  "expiry_datetime": "2025-11-04T19:45:30.123456"
}
```

## 🔄 토큰 생명주기

### 토큰 발급
```python
# KISClient 초기화 시 자동으로 TokenManager 생성
client = KISClient(
    app_key="your_app_key",
    app_secret="your_app_secret",
    account_number="12345678",
    account_code="01",
    trading_mode="MOCK"
)

# API 호출 시 자동으로 토큰 확보
balance = await client.get_account_balance()
```

### 토큰 재사용
- 같은 `app_key`와 `trading_mode`를 사용하면 저장된 토큰 자동 재사용
- 유효기간이 남아있으면 API 재발급 없이 파일에서 로드

### 토큰 만료 및 재발급
- 토큰 만료 5분 전부터 "만료"로 간주 (안전 버퍼)
- 만료된 토큰 감지 시 자동으로 새 토큰 요청
- 새 토큰 발급 시 파일 자동 갱신

## 📊 로깅

토큰 관리 과정은 상세하게 로깅됩니다:

```
2025-11-03 19:45:30 - INFO - [TokenManager] Initialized for mock mode
2025-11-03 19:45:30 - INFO - [TokenManager] Token file: ~/KIS/tokens/token_PStoMm5NMd_mock.json
2025-11-03 19:45:30 - INFO - [KISClient] Checking for cached token...
2025-11-03 19:45:30 - INFO - [TokenManager] No token file found
2025-11-03 19:45:30 - INFO - [KISClient] No valid cached token, requesting new token...
2025-11-03 19:45:31 - INFO - [KIS API] Requesting new access token
2025-11-03 19:45:31 - INFO - [KIS API] Response Status: 200
2025-11-03 19:45:31 - INFO - [KIS API] Access token obtained successfully
2025-11-03 19:45:31 - INFO - [TokenManager] Token saved successfully
2025-11-03 19:45:31 - INFO - [TokenManager]   - Issued at: 2025-11-03 19:45:31
2025-11-03 19:45:31 - INFO - [TokenManager]   - Expires at: 2025-11-04 19:45:31
2025-11-03 19:45:31 - INFO - [TokenManager]   - Valid for: 86400 seconds
```

## 🔒 보안 고려사항

### 토큰 파일 위치
- 기본 위치: `~/KIS/tokens/` (사용자 홈 디렉토리)
- 파일 권한: 자동으로 사용자만 읽기/쓰기 가능
- 제3자가 접근하기 어려운 위치에 저장 권장

### 민감 정보 로깅
- App Key, App Secret은 처음 10자만 로그에 기록
- Access Token은 로그에 기록하지 않음
- 토큰 파일 경로만 로그에 표시

## 🧪 테스트

### 토큰 파일 확인
```bash
# 토큰 파일 목록 확인
ls -la ~/KIS/tokens/

# 토큰 파일 내용 확인 (JSON 포맷)
cat ~/KIS/tokens/token_PStoMm5NMd_mock.json | python -m json.tool
```

### 토큰 삭제 (강제 재발급 테스트)
```bash
# 모든 토큰 파일 삭제
rm -rf ~/KIS/tokens/*.json

# 특정 토큰만 삭제
rm ~/KIS/tokens/token_PStoMm5NMd_mock.json
```

### 로그 확인
```bash
# 토큰 관련 로그만 보기
grep "Token" backend/logs/app.log

# KIS API 호출 로그
grep "KIS API" backend/logs/app.log
```

## 🔧 설정

### 토큰 유효기간 버퍼 조정

기본적으로 토큰 만료 5분 전부터 재발급합니다. 이를 조정하려면:

```python
# kis_token_manager.py의 is_expired 메서드
def is_expired(self, buffer_seconds: int = 300) -> bool:
    # buffer_seconds를 원하는 값으로 변경 (초 단위)
    # 예: 600 = 10분 전부터 재발급
    pass
```

### 토큰 저장 위치 변경

```python
# kis_token_manager.py의 __init__ 메서드
self.token_dir = Path.home() / "KIS" / "tokens"
# 원하는 경로로 변경:
# self.token_dir = Path("/path/to/your/token/dir")
```

## 📈 성능 개선

### 개선 효과

1. **API 호출 감소**: 매번 토큰 재발급하지 않고 파일에서 재사용
2. **응답 속도 향상**: 토큰 발급 API 호출 생략 (약 200-500ms 절약)
3. **안정성 향상**: KIS API의 "1분당 1회 발급" 제한 회피

### 토큰 재사용 시나리오

```
시나리오 1: 첫 API 호출
- 토큰 파일 없음 → API 요청 (500ms) → 파일 저장
총 시간: ~500ms

시나리오 2: 이후 API 호출 (토큰 유효)
- 토큰 파일 로드 (1ms) → 메모리 사용
총 시간: ~1ms (500배 빠름!)

시나리오 3: 토큰 만료 후 API 호출
- 토큰 파일 로드 → 만료 감지 → API 재발급 (500ms) → 파일 갱신
총 시간: ~500ms
```

## 🐛 문제 해결

### 토큰 파일이 생성되지 않음

**확인 사항:**
1. `~/KIS/tokens/` 디렉토리가 생성되었는가?
   ```bash
   ls -la ~/KIS/
   ```
2. 디렉토리 쓰기 권한이 있는가?
   ```bash
   touch ~/KIS/tokens/test.txt && rm ~/KIS/tokens/test.txt
   ```

### 토큰이 계속 재발급됨

**원인:**
- 토큰 파일이 삭제되었거나 손상됨
- 시스템 시간이 잘못 설정됨
- `issued_at` 시간 파싱 오류

**해결:**
```bash
# 토큰 파일 확인
cat ~/KIS/tokens/token_*.json

# 시스템 시간 확인
date
```

### 403 Forbidden 에러

**원인:**
- App Key/Secret이 잘못됨
- IP 화이트리스트 미등록 (실전투자의 경우)
- API 권한 부족

**해결:**
1. App Key/Secret 재확인
2. KIS 개발자 센터에서 IP 등록
3. 로그 확인:
   ```bash
   tail -f backend/logs/app.log | grep "KIS API"
   ```

## 📝 변경 이력

### 2025-11-03
- KISTokenManager 클래스 생성
- KISToken 모델 업데이트 (파일 저장용)
- KISClient에 토큰 캐싱 로직 추가
- 토큰 파일 저장/로드 기능 구현
- 토큰 만료 자동 감지 및 재발급

---

**참고 문서:**
- KIS Open API GitHub: https://github.com/koreainvestment/open-trading-api
- kis_auth.py 참고: https://github.com/koreainvestment/open-trading-api/blob/main/examples_user/kis_auth.py

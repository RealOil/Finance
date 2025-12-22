# API 실패 시나리오 처리

## 현재 요구사항 문서의 관련 내용

### 기존 명시 사항

- API 호출 실패 시 graceful degradation (기본값 사용) (3.1 성능)
- API 호출 제한에 따른 데이터 업데이트 주기 제한 가능 (6.1 제약사항)
- 과거 데이터 조회 실패 시, 평균값 또는 추정값 사용 (명시) (2.2.2)

---

## 추가 확인 필요 사항

### 1. API 호출 실패 시 기본값

**문제 상황**:

- 한국은행 API 서버 다운
- 네트워크 오류
- API 키 만료 또는 제한 초과
- API 응답 지연 (타임아웃)

**제안**:

#### 기본값 전략

| 데이터 타입         | 기본값                          | 근거                                  |
| ------------------- | ------------------------------- | ------------------------------------- |
| 인플레이션          | 최근 3년 평균 (2.5%)            | 한국은행 목표 인플레이션 2% + 여유    |
| 환율 (USD)          | 최근 1개월 평균                 | 환율은 변동성이 크므로 최근 평균 사용 |
| 환율 (EUR, JPY)     | 최근 1개월 평균                 | 동일                                  |
| 암호화폐 (BTC, ETH) | 사용자 입력 또는 최근 7일 평균  | 변동성이 매우 크므로 사용자 입력 우선 |
| 주식 지수           | 최근 1개월 평균                 | 변동성 고려                           |
| 금리                | 한국은행 기준금리 (최근 발표값) | 공개 정보 활용                        |

#### 구현 방법

```python
import requests
from datetime import datetime, timedelta
import json

# 캐시된 데이터 파일 경로
CACHE_FILE = "api_cache.json"
CACHE_DURATION = timedelta(hours=24)  # 24시간 캐시

def get_inflation_rate():
    """인플레이션 데이터 조회 (실패 시 기본값)"""
    try:
        # API 호출 시도
        response = requests.get(
            "https://ecos.bok.or.kr/api/...",
            timeout=5  # 5초 타임아웃
        )
        if response.status_code == 200:
            data = response.json()
            # 캐시에 저장
            save_to_cache('inflation', data)
            return data['value']
    except (requests.Timeout, requests.ConnectionError, requests.RequestException) as e:
        st.warning("⚠️ 인플레이션 데이터를 가져올 수 없습니다. 기본값을 사용합니다.")

        # 캐시 확인
        cached_data = load_from_cache('inflation')
        if cached_data:
            return cached_data['value']

        # 최종 기본값
        return 2.5  # 최근 3년 평균 인플레이션

    # 최종 기본값
    return 2.5

def save_to_cache(key, value):
    """캐시에 데이터 저장"""
    try:
        cache = {}
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)

        cache[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }

        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except Exception:
        pass  # 캐시 실패해도 계속 진행

def load_from_cache(key):
    """캐시에서 데이터 로드"""
    try:
        if not os.path.exists(CACHE_FILE):
            return None

        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)

        if key not in cache:
            return None

        cached_item = cache[key]
        timestamp = datetime.fromisoformat(cached_item['timestamp'])

        # 캐시 유효성 확인 (24시간)
        if datetime.now() - timestamp > CACHE_DURATION:
            return None

        return cached_item
    except Exception:
        return None
```

---

### 2. 오프라인 모드

**문제 상황**:

- 인터넷 연결이 없는 환경
- API 서버가 완전히 다운
- 사용자가 오프라인에서도 기본 기능 사용 원함

**제안**:

#### 오프라인 모드 지원

- **기본 계산 기능**: 오프라인에서도 동작
  - 소득 및 지출 기반 인사이트 (API 불필요)
  - 미래 리스크 시나리오 (API 불필요)
- **API 의존 기능**: 오프라인에서 비활성화 또는 기본값 사용
  - 인플레이션 반영 계산 → 기본값 사용
  - 환율 계산 → 기본값 사용
  - 실시간 주가/암호화폐 → 기능 비활성화

#### 구현 방법

```python
def check_online():
    """인터넷 연결 확인"""
    try:
        response = requests.get("https://www.google.com", timeout=3)
        return response.status_code == 200
    except:
        return False

# 앱 시작 시 확인
is_online = check_online()

if not is_online:
    st.warning("""
    ⚠️ **오프라인 모드**

    인터넷 연결이 없습니다. 다음 기능은 제한됩니다:
    - 실시간 환율/인플레이션 데이터
    - 주가/암호화폐 가격

    기본 계산 기능은 정상적으로 작동합니다.
    """)

    # 오프라인 모드 플래그 설정
    st.session_state['offline_mode'] = True
else:
    st.session_state['offline_mode'] = False
```

---

### 3. API Rate Limit 처리

**문제 상황**:

- API 호출 제한 초과 (예: 분당 10회)
- 여러 사용자가 동시에 접근 시 제한
- 무료 API의 제한적 호출 횟수

**제안**:

#### Rate Limiting 전략

**옵션 A: 캐싱 우선 (추천)**

- API 호출 전에 캐시 확인
- 캐시가 유효하면 API 호출 생략
- 캐시 만료 시에만 API 호출

**옵션 B: 배치 처리**

- 여러 데이터를 한 번에 요청
- API 호출 횟수 최소화

**옵션 C: 사용자별 제한**

- 사용자당 일일 호출 횟수 제한
- 초과 시 기본값 사용

#### 구현 방법

```python
import time
from collections import defaultdict

# Rate limiter 클래스
class RateLimiter:
    def __init__(self, max_calls=10, period=60):
        self.max_calls = max_calls
        self.period = period
        self.calls = defaultdict(list)

    def can_call(self, api_name):
        """호출 가능한지 확인"""
        now = time.time()
        # 최근 period 초간의 호출 기록
        recent_calls = [
            call_time for call_time in self.calls[api_name]
            if now - call_time < self.period
        ]

        if len(recent_calls) >= self.max_calls:
            return False

        return True

    def record_call(self, api_name):
        """호출 기록"""
        self.calls[api_name].append(time.time())
        # 오래된 기록 정리
        now = time.time()
        self.calls[api_name] = [
            call_time for call_time in self.calls[api_name]
            if now - call_time < self.period
        ]

# 전역 Rate Limiter
rate_limiter = RateLimiter(max_calls=10, period=60)

def safe_api_call(api_name, api_func, default_value):
    """안전한 API 호출 (Rate Limit 고려)"""
    # 캐시 확인
    cached = load_from_cache(api_name)
    if cached:
        return cached['value']

    # Rate Limit 확인
    if not rate_limiter.can_call(api_name):
        st.warning(f"⚠️ {api_name} API 호출 제한에 도달했습니다. 기본값을 사용합니다.")
        return default_value

    try:
        result = api_func()
        rate_limiter.record_call(api_name)
        save_to_cache(api_name, result)
        return result
    except Exception as e:
        st.warning(f"⚠️ {api_name} API 호출 실패: {str(e)}. 기본값을 사용합니다.")
        return default_value
```

---

### 4. 타임아웃 처리

**문제 상황**:

- API 응답이 느림 (5초 이상)
- 사용자 대기 시간 증가
- 전체 앱 성능 저하

**제안**:

#### 타임아웃 설정

- **일반 API**: 3초 타임아웃
- **중요 API**: 5초 타임아웃
- 타임아웃 발생 시 즉시 기본값 사용

#### 구현 방법

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session_with_retry():
    """재시도 로직이 있는 세션 생성"""
    session = requests.Session()

    retry_strategy = Retry(
        total=2,  # 최대 2번 재시도
        backoff_factor=0.3,  # 재시도 간격
        status_forcelist=[429, 500, 502, 503, 504],  # 재시도할 HTTP 상태 코드
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session

# 사용 예시
session = create_session_with_retry()

try:
    response = session.get(
        "https://api.example.com/data",
        timeout=3  # 3초 타임아웃
    )
    data = response.json()
except requests.Timeout:
    st.warning("API 응답이 지연됩니다. 기본값을 사용합니다.")
    data = get_default_value()
except requests.RequestException as e:
    st.warning(f"API 호출 실패: {str(e)}. 기본값을 사용합니다.")
    data = get_default_value()
```

---

### 5. 사용자 알림 및 투명성

**문제 상황**:

- API 실패 시 사용자가 모름
- 기본값 사용 시 신뢰도 저하
- 데이터 출처 불명확

**제안**:

#### 명확한 알림 표시

- API 실패 시 상단에 경고 배너 표시
- 기본값 사용 시 "기본값 사용 중" 표시
- 데이터 출처 및 업데이트 시간 표시

#### 구현 예시

```python
# API 상태 표시
api_status = {
    'inflation': {'status': 'success', 'last_update': '2024-01-15 10:30'},
    'exchange_rate': {'status': 'cached', 'last_update': '2024-01-14 15:20'},
    'crypto': {'status': 'failed', 'last_update': None}
}

# 상태 표시 UI
st.sidebar.markdown("### 📊 데이터 상태")

for api_name, status_info in api_status.items():
    if status_info['status'] == 'success':
        st.sidebar.success(f"✅ {api_name}: 최신 데이터")
    elif status_info['status'] == 'cached':
        st.sidebar.info(f"💾 {api_name}: 캐시된 데이터 ({status_info['last_update']})")
    else:
        st.sidebar.warning(f"⚠️ {api_name}: 기본값 사용 중")

# 결과 페이지에 데이터 출처 표시
st.markdown("---")
st.caption(f"💡 인플레이션 데이터: 한국은행 (2024-01-15 기준, 기본값 사용)")
```

---

## 구현 우선순위

### Phase 1 (필수)

1. ✅ 기본값 정의 및 적용
2. ✅ 타임아웃 처리 (3초)
3. ✅ 기본 에러 핸들링 (try-except)
4. ✅ 사용자 알림 (기본값 사용 시 경고)

### Phase 2 (권장)

5. ⚠️ 캐싱 시스템 구현
6. ⚠️ Rate Limiting 처리
7. ⚠️ 오프라인 모드 지원
8. ⚠️ 재시도 로직
9. ⚠️ 상세한 상태 표시

---

## 사용자 경험 원칙

1. **투명성**: API 실패 시 명확히 알림
2. **연속성**: 기본값으로라도 기능 계속 제공
3. **신뢰성**: 데이터 출처 및 업데이트 시간 명시
4. **성능**: 타임아웃으로 빠른 응답 보장

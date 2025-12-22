# 데이터 보안 및 개인정보

## 현재 요구사항 문서의 관련 내용

### 기존 명시 사항

- 개인 금융 정보 로컬 처리 (서버 전송 최소화) (3.4 보안 및 개인정보)
- API 키는 환경 변수로 관리 (3.4 보안 및 개인정보)
- 개인정보 수집 최소화 (필수 입력만) (3.4 보안 및 개인정보)

---

## 추가 확인 필요 사항

### 1. 개인정보 처리방침

**문제 상황**:

- 사용자 데이터 수집/저장/삭제 정책 불명확
- 법적 요구사항 (개인정보보호법) 준수 필요
- 사용자 신뢰 확보 필요

**제안**:

#### 개인정보 처리방침 내용

**수집 항목**:

- 필수: 나이, 연봉, 지출, 자산, 부채 (계산에 필수)
- 선택: 보너스, 라이프스타일 지출 등 (사용자 선택)

**수집 목적**:

- 재정 시뮬레이션 및 분석
- 개인화된 인사이트 제공

**보관 기간**:

- **Streamlit Cloud**: 세션 종료 시 즉시 삭제
- **로컬 파일**: 사용자가 직접 삭제
- **Notion**: 사용자가 직접 관리 (영구 보관 가능)

**제3자 제공**:

- 제공하지 않음 (명시)
- API 호출 시 필요한 최소 정보만 전송 (예: 환율 조회 시 금액은 전송하지 않음)

#### 구현 방법

```python
# 앱 시작 시 개인정보 처리방침 표시
if 'privacy_accepted' not in st.session_state:
    with st.container():
        st.markdown("""
        ## 개인정보 처리방침

        ### 수집하는 정보
        - 필수: 나이, 연봉, 지출, 자산, 부채
        - 선택: 보너스, 라이프스타일 지출 등

        ### 보관 및 삭제
        - 모든 데이터는 브라우저 세션에만 저장됩니다
        - 브라우저를 닫으면 데이터가 삭제됩니다
        - 서버에 저장되지 않습니다

        ### 제3자 제공
        - 제공하지 않습니다
        - API 호출 시에도 개인 정보는 전송되지 않습니다

        [전체 개인정보 처리방침 보기](링크)
        """)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("동의하고 시작하기"):
                st.session_state.privacy_accepted = True
                st.rerun()
        with col2:
            if st.button("거부"):
                st.stop()
```

---

### 2. 데이터 암호화

**문제 상황**:

- 전송 중 데이터 노출 위험
- 저장된 데이터 보호 필요
- 로컬 파일 보안

**제안**:

#### 전송 암호화

- **HTTPS 필수**: Streamlit Cloud는 기본 HTTPS
- **API 호출**: 모든 API는 HTTPS로 호출

#### 저장 암호화 (선택)

- **로컬 파일**: 민감 정보는 암호화 저장 (선택적)
- **Notion**: Notion의 기본 보안 기능 활용

#### 구현 방법

```python
from cryptography.fernet import Fernet
import base64
import os

def get_encryption_key():
    """암호화 키 생성 또는 로드"""
    key_file = ".encryption_key"

    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        # 새 키 생성 (로컬 환경에서만)
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

def encrypt_data(data):
    """데이터 암호화 (선택적)"""
    if not st.session_state.get('enable_encryption', False):
        return data

    key = get_encryption_key()
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_data(encrypted_data):
    """데이터 복호화"""
    key = get_encryption_key()
    f = Fernet(key)
    decrypted = f.decrypt(base64.b64decode(encrypted_data))
    return decrypted.decode()
```

**참고**: Phase 1에서는 암호화는 선택적. Phase 2에서 고려.

---

### 3. 쿠키 및 로컬 스토리지

**문제 상황**:

- 브라우저 쿠키 사용 여부
- 로컬 스토리지에 데이터 저장 여부
- 사용자 추적 가능성

**제안**:

#### 쿠키 정책

- **필수 쿠키**: 없음 (Streamlit 세션은 서버 측)
- **선택 쿠키**: 사용자 설정 저장 (예: 튜토리얼 완료 여부)

#### 로컬 스토리지

- **옵션 A: 사용 안 함 (추천 Phase 1)**

  - 모든 데이터는 세션에만 저장
  - 브라우저 종료 시 삭제
  - 가장 안전

- **옵션 B: 선택적 사용 (Phase 2)**
  - 사용자가 명시적으로 요청 시에만 저장
  - 암호화하여 저장
  - 언제든지 삭제 가능

#### 구현 방법

```python
# Streamlit 세션 상태 사용 (서버 측, 쿠키 아님)
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# 로컬 스토리지 사용 (선택적, Phase 2)
if st.checkbox("데이터를 브라우저에 저장 (다음 방문 시 자동 로드)"):
    # JavaScript를 통한 로컬 스토리지 저장
    st.markdown("""
    <script>
    localStorage.setItem('finance_data', JSON.stringify(data));
    </script>
    """, unsafe_allow_html=True)
```

---

### 4. API 키 보안

**문제 상황**:

- API 키가 코드에 노출
- GitHub에 공개 저장 시 키 유출
- 무단 사용 방지

**제안**:

#### 환경 변수 사용 (필수)

- 모든 API 키는 환경 변수로 관리
- `.env` 파일 사용 (Git에 커밋하지 않음)
- Streamlit Cloud Secrets 사용

#### 구현 방법

```python
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 키 가져오기
BOK_API_KEY = os.getenv('BOK_API_KEY')
COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY', None)  # 선택적

# Streamlit Cloud Secrets 사용 (배포 시)
if 'BOK_API_KEY' in st.secrets:
    BOK_API_KEY = st.secrets['BOK_API_KEY']
```

#### .gitignore 설정

```
.env
.env.local
*.key
secrets/
```

#### Streamlit Cloud Secrets 설정

1. Streamlit Cloud 대시보드 접속
2. Settings → Secrets
3. API 키 추가:

```toml
[BOK]
api_key = "your-api-key-here"

[COINGECKO]
api_key = "your-api-key-here"
```

---

### 5. 데이터 삭제 기능

**문제 상황**:

- 사용자가 데이터를 삭제하고 싶을 때
- 로컬 파일 삭제 방법
- Notion 데이터 삭제

**제안**:

#### 데이터 삭제 기능 제공

- **세션 데이터**: "모든 데이터 초기화" 버튼
- **로컬 파일**: 파일 삭제 가이드 제공
- **Notion**: 사용자가 직접 삭제 (가이드 제공)

#### 구현 방법

```python
# 사이드바에 삭제 버튼
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚠️ 데이터 관리")

if st.sidebar.button("모든 데이터 초기화", type="secondary"):
    # 확인 다이얼로그
    if st.sidebar.checkbox("정말로 모든 데이터를 삭제하시겠습니까?"):
        # 세션 상태 초기화
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
```

---

### 6. 접근 제어 (선택)

**문제 상황**:

- 개인정보 보호를 위한 접근 제어
- 사용자 인증 필요 여부
- 공개 vs 비공개 앱

**제안**:

#### Phase 1: 공개 앱 (추천)

- 별도 인증 없이 사용
- 모든 데이터는 로컬/세션에만 저장
- 서버에 저장하지 않음

#### Phase 2: 선택적 인증

- 사용자가 원할 경우 계정 생성
- 데이터 클라우드 저장 (암호화)
- 여러 기기에서 동기화

---

## 구현 우선순위

### Phase 1 (필수)

1. ✅ 개인정보 처리방침 명시
2. ✅ API 키 환경 변수 관리
3. ✅ HTTPS 사용 (Streamlit Cloud 기본)
4. ✅ 데이터 삭제 기능

### Phase 2 (권장)

5. ⚠️ 로컬 파일 암호화 (선택적)
6. ⚠️ 사용자 인증 (선택적)
7. ⚠️ 접근 로그 (선택적)

---

## 법적 고지

### 개인정보보호법 준수

- 수집 목적 명시
- 보관 기간 명시
- 삭제 방법 제공
- 제3자 제공 금지 명시

### 금융 관련 법규

- 금융 조언이 아님을 명시
- 투자 권유 금지
- 면책 조항 포함

---

## 사용자 신뢰 확보 원칙

1. **투명성**: 데이터 사용 목적 명확히 공개
2. **최소 수집**: 필요한 최소한의 정보만 수집
3. **사용자 제어**: 언제든지 데이터 삭제 가능
4. **보안**: 전송 및 저장 시 보안 조치

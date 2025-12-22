# Phase 1 MVP 상세 디자인

## 개요

### 목표

- **기간**: 4~6주
- **기능**: 소득 및 지출 기반 인사이트 + 미래 리스크 및 시나리오 경고
- **플랫폼**: Streamlit Cloud 배포
- **목표**: 핵심 기능 검증 및 사용자 피드백 수집

---

## 1. 전체 아키텍처

### 1.1 시스템 구조

```
┌─────────────────────────────────────────┐
│         사용자 (브라우저)                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Streamlit Cloud (배포 환경)        │
│  ┌──────────────────────────────────┐  │
│  │   Streamlit App (main.py)        │  │
│  │  - UI 렌더링                      │  │
│  │  - 사용자 입력 처리               │  │
│  │  - 계산 로직                      │  │
│  │  - 결과 시각화                    │  │
│  └──────────┬───────────────────────┘  │
│             │                           │
│  ┌──────────▼───────────────────────┐  │
│  │   계산 모듈 (calculations.py)     │  │
│  │  - 자산 시뮬레이션                │  │
│  │  - 리스크 계산                    │  │
│  │  - 시나리오 비교                  │  │
│  └──────────┬───────────────────────┘  │
│             │                           │
│  ┌──────────▼───────────────────────┐  │
│  │   유틸리티 (utils.py)            │  │
│  │  - 입력 검증                     │  │
│  │  - 데이터 정제                   │  │
│  │  - 포맷팅                        │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      외부 API (선택적)                  │
│  - 한국은행 인플레이션 API (기본값 사용) │
└─────────────────────────────────────────┘
```

### 1.2 파일 구조

```
finance-simulator/
├── app.py                 # 메인 홈 페이지 (소개 및 네비게이션)
├── pages/                 # 기능별 페이지 (Streamlit pages 자동 인식)
│   ├── 1_소득_지출_분석.py      # 소득 및 지출 기반 인사이트
│   ├── 2_리스크_시나리오.py     # 미래 리스크 및 시나리오 경고
│   └── 3_시나리오_비교.py       # 시나리오 비교 (선택적, Phase 1 후반)
├── modules/
│   ├── calculations.py   # 계산 로직
│   ├── validators.py     # 입력 검증
│   ├── formatters.py     # 데이터 포맷팅
│   └── visualizations.py # 시각화 생성
├── shared/                # 공통 모듈
│   ├── input_form.py     # 공통 입력 폼 컴포넌트
│   └── session_manager.py # 세션 상태 관리
├── data/
│   └── defaults.py      # 기본값 정의
├── config/
│   └── constants.py     # 상수 정의
├── requirements.txt      # Python 패키지
├── .env.example         # 환경 변수 예시
├── .gitignore
├── README.md
└── docs/
    └── (기존 문서들)
```

**페이지 명명 규칙**:

- 숫자 접두사로 순서 지정 (1*, 2*, 3\_)
- 한글 이름 사용 (Streamlit이 자동으로 사이드바에 표시)
- Phase 2 추가 시 4*, 5*... 순서로 추가

---

## 2. UI/UX 디자인

### 2.1 페이지 구조 (멀티 페이지)

#### 전체 페이지 구조

```
┌─────────────────────────────────────────────────────┐
│  📊 경제적 자유 시뮬레이터                    [설정] │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [사이드바 네비게이션]    [현재 페이지 콘텐츠]      │
│  ┌──────────────────┐   ┌──────────────────────┐  │
│  │ 🏠 홈            │   │                      │  │
│  │ 📊 소득 지출 분석 │   │  [페이지별 콘텐츠]    │  │
│  │ ⚠️ 리스크 시나리오│   │                      │  │
│  │ 📈 시나리오 비교  │   │                      │  │
│  │                  │   │                      │  │
│  │ [샘플 데이터]     │   │                      │  │
│  │ [피드백]         │   │                      │  │
│  └──────────────────┘   └──────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**페이지 구성**:

1. **홈 (app.py)**: 프로젝트 소개, 빠른 시작 가이드
2. **소득 지출 분석 (pages/1*소득*지출\_분석.py)**: 소득 및 지출 기반 인사이트
3. **리스크 시나리오 (pages/2*리스크*시나리오.py)**: 미래 리스크 분석
4. **시나리오 비교 (pages/3*시나리오*비교.py)**: 여러 시나리오 비교 (선택적)

### 2.2 홈 페이지 (app.py)

```python
import streamlit as st

st.set_page_config(
    page_title="경제적 자유 시뮬레이터",
    page_icon="📊",
    layout="wide"
)

st.title("📊 경제적 자유 시뮬레이터")
st.markdown("---")

st.markdown("""
## 환영합니다! 👋

이 도구는 여러분의 재정 상황을 분석하고 미래를 시뮬레이션합니다.

### 🎯 주요 기능

#### 1. 📊 소득 및 지출 분석
- 현재 소비 패턴 유지 시 미래 자산 예측
- 재정 건전성 등급 평가
- 시나리오별 비교

#### 2. ⚠️ 리스크 시나리오
- 소득 중단 시 생존 가능 기간
- 경제 위기 시나리오 분석
- 은퇴 준비 상태 확인

### 🚀 빠른 시작

1. 왼쪽 사이드바에서 원하는 기능 선택
2. 기본 정보 입력
3. 계산 결과 확인

### 💡 팁

- 처음 사용하시나요? 샘플 데이터로 먼저 시도해보세요!
- 각 페이지는 독립적으로 작동합니다
- 입력한 데이터는 브라우저를 닫으면 삭제됩니다
""")

# 빠른 링크
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 소득 지출 분석 시작", use_container_width=True):
        st.switch_page("pages/1_소득_지출_분석.py")
with col2:
    if st.button("⚠️ 리스크 시나리오 시작", use_container_width=True):
        st.switch_page("pages/2_리스크_시나리오.py")
with col3:
    if st.button("📈 시나리오 비교 시작", use_container_width=True):
        st.switch_page("pages/3_시나리오_비교.py")
```

### 2.3 공통 입력 폼 컴포넌트 (shared/input_form.py)

모든 페이지에서 공통으로 사용하는 입력 폼을 컴포넌트로 분리:

```python
import streamlit as st

def render_input_form():
    """
    공통 입력 폼 렌더링
    모든 페이지에서 동일한 입력 폼 사용
    """
    st.sidebar.markdown("### 📋 기본 정보")

    current_age = st.sidebar.number_input(
        "현재 나이",
        min_value=0,
        max_value=150,
        value=st.session_state.get('current_age', 30),
        help="만 나이를 입력하세요"
    )

    retirement_age = st.sidebar.number_input(
        "기대 은퇴 나이",
        min_value=current_age + 1 if current_age else 1,
        max_value=100,
        value=st.session_state.get('retirement_age', 60),
        help="은퇴를 계획하는 나이입니다"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💰 소득 정보")

    salary = st.sidebar.number_input(
        "연봉 (만원)",
        min_value=0,
        value=st.session_state.get('salary', 5000),
        step=100,
        help="세전 연봉을 입력하세요"
    )

    salary_growth_rate = st.sidebar.slider(
        "연평균 소득 증가율 (%)",
        min_value=0.0,
        max_value=20.0,
        value=st.session_state.get('salary_growth_rate', 3.0),
        step=0.5,
        help="매년 연봉이 증가하는 비율"
    )

    bonus = st.sidebar.number_input(
        "보너스 (만원/년, 선택)",
        min_value=0,
        value=st.session_state.get('bonus', 0),
        step=100
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💸 소비 정보")

    monthly_expense = st.sidebar.number_input(
        "월 지출 (만원)",
        min_value=0,
        value=st.session_state.get('monthly_expense', 200),
        step=10,
        help="월 평균 지출액입니다"
    )

    annual_fixed_expense = st.sidebar.number_input(
        "연간 고정 지출 (만원, 선택)",
        min_value=0,
        value=st.session_state.get('annual_fixed_expense', 0),
        step=100,
        help="보험료, 세금 등 연간 고정 지출"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏦 자산 및 부채")

    total_assets = st.sidebar.number_input(
        "현재 총 자산 (만원)",
        min_value=0,
        value=st.session_state.get('total_assets', 1000),
        step=100,
        help="예금, 적금, 주식 등 모든 자산의 합계"
    )

    total_debt = st.sidebar.number_input(
        "현재 총 부채 (만원)",
        min_value=0,
        value=st.session_state.get('total_debt', 0),
        step=100,
        help="대출, 신용카드 빚 등 모든 부채의 합계"
    )

    # 세션 상태에 저장
    inputs = {
        'current_age': current_age,
        'retirement_age': retirement_age,
        'salary': salary,
        'salary_growth_rate': salary_growth_rate,
        'bonus': bonus,
        'monthly_expense': monthly_expense,
        'annual_fixed_expense': annual_fixed_expense,
        'total_assets': total_assets,
        'total_debt': total_debt
    }

    # 세션 상태 업데이트
    for key, value in inputs.items():
        st.session_state[key] = value

    return inputs
```

### 2.4 페이지별 레이아웃

#### 페이지 1: 소득 지출 분석 (pages/1*소득*지출\_분석.py)

#### 섹션 1: 기본 정보

```python
st.sidebar.markdown("### 📋 기본 정보")

current_age = st.sidebar.number_input(
    "현재 나이",
    min_value=0,
    max_value=150,
    value=30,
    help="만 나이를 입력하세요"
)

retirement_age = st.sidebar.number_input(
    "기대 은퇴 나이",
    min_value=current_age + 1 if current_age else 1,
    max_value=100,
    value=60,
    help="은퇴를 계획하는 나이입니다"
)
```

#### 섹션 2: 소득 정보

```python
st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 소득 정보")

salary = st.sidebar.number_input(
    "연봉 (만원)",
    min_value=0,
    value=5000,
    step=100,
    help="세전 연봉을 입력하세요"
)

salary_growth_rate = st.sidebar.slider(
    "연평균 소득 증가율 (%)",
    min_value=0.0,
    max_value=20.0,
    value=3.0,
    step=0.5,
    help="매년 연봉이 증가하는 비율"
)

bonus = st.sidebar.number_input(
    "보너스 (만원/년, 선택)",
    min_value=0,
    value=0,
    step=100
)
```

#### 섹션 3: 소비 정보

```python
st.subheader("소비 정보")

monthly_fixed_expense = st.number_input(
    "월간 고정비 (만원)",
    min_value=0,
    value=None,  # 초기값은 빈 값
    step=10,
    help="주거비, 보험료, 통신비, 대출이자 등 고정 지출"
)

monthly_variable_expense = st.number_input(
    "월간 변동비 (만원)",
    min_value=0,
    value=None,  # 초기값은 빈 값
    step=10,
    help="식비, 교통비, 여가비, 쇼핑 등 변동 지출"
)

# 총 월 지출 표시 (읽기 전용)
monthly_total_expense = monthly_fixed_expense + monthly_variable_expense
st.metric("총 월 지출", format_currency(monthly_total_expense))
```

#### 섹션 4: 자산 및 부채

```python
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏦 자산 및 부채")

total_assets = st.sidebar.number_input(
    "현재 총 자산 (만원)",
    min_value=0,
    value=1000,
    step=100,
    help="예금, 적금, 주식 등 모든 자산의 합계"
)

total_debt = st.sidebar.number_input(
    "현재 총 부채 (만원)",
    min_value=0,
    value=0,
    step=100,
    help="대출, 신용카드 빚 등 모든 부채의 합계"
)
```

#### 계산 버튼

```python
st.sidebar.markdown("---")

# 입력 검증
is_valid = validate_inputs(
    current_age, retirement_age, salary,
    monthly_expense, total_assets, total_debt
)

if is_valid:
    calculate_button = st.sidebar.button(
        "🚀 계산하기",
        type="primary",
        use_container_width=True
    )
else:
    st.sidebar.warning("모든 필수 항목을 입력해주세요")
    calculate_button = st.sidebar.button(
        "🚀 계산하기",
        disabled=True,
        use_container_width=True
    )
```

### 2.5 Phase 2 확장을 위한 페이지 구조

**장점**:

- 각 기능이 독립적인 페이지로 분리되어 유지보수 용이
- Phase 2에서 새 기능 추가 시 `pages/4_새기능.py` 형태로 쉽게 추가
- 사용자가 원하는 기능만 선택하여 사용 가능
- 각 페이지의 로딩 속도 개선 (필요한 모듈만 로드)

**Phase 2 추가 예시**:

```
pages/
├── 1_소득_지출_분석.py      # Phase 1
├── 2_리스크_시나리오.py     # Phase 1
├── 3_시나리오_비교.py       # Phase 1
├── 4_기회비용_분석.py       # Phase 2 (우선순위 3)
├── 5_부동산_분석.py         # Phase 2 (우선순위 4)
├── 6_보험_분석.py           # Phase 2 (우선순위 5)
└── ...
```

---

## 3. 핵심 기능 상세 스펙

### 3.1 소득 및 지출 기반 인사이트

#### 기능 1: 미래 자산 추정

**입력**:

- 현재 자산
- 연봉
- 월간 고정비, 월간 변동비
- 연봉 증가율
- 인플레이션율 (사용자 입력, 기본값 2.5%)
- 은퇴 후 생활비, 의료비
- 시뮬레이션 기간: 은퇴 전 기간 + 은퇴 후 기간 (평균 수명까지)

**데이터 출처**:

- 입력 데이터: 사용자 직접 입력
- 연봉 증가율: 사용자 입력 (기본값 3%, 통계청 평균 참고)
- 인플레이션율: 사용자 입력 (기본값 2.5%, 한국은행 최근 3년 평균)
- 은퇴 후 생활비: 가구 형태에 따른 평균값 (부부: 318만원, 1인: 170만원)
- 은퇴 후 의료비: 65세 이상 평균 월 45만원
- 평균 수명: 83세 (한국 평균 기대수명)

**계산 가정**:

- 인플레이션 반영 (고정비, 변동비 모두 적용)
- 투자 수익 미고려 (저축만 고려)
- 은퇴 후 기간: 평균 수명(83세)까지 계산
- 은퇴 후 소득 없음, 생활비와 의료비만 지출

**계산 로직**:

```python
def calculate_future_assets(
    current_assets: float,
    annual_salary: float,
    monthly_expense: float,
    salary_growth_rate: float,
    years: int = 10
) -> list:
    """
    연도별 자산 변화 계산

    Returns:
        list: 각 연도의 자산 리스트
    """
    assets = [current_assets]
    current_salary = annual_salary

    for year in range(1, years + 1):
        # 연봉 증가
        current_salary *= (1 + salary_growth_rate / 100)

        # 연간 소득
        annual_income = current_salary

        # 연간 지출
        annual_expense = monthly_expense * 12

        # 연간 저축
        annual_savings = annual_income - annual_expense

        # 다음 해 자산
        next_assets = assets[-1] + annual_savings
        assets.append(next_assets)

    return assets
```

**출력**:

- 나이별 자산 리스트 (은퇴 전 + 은퇴 후)
- 최종 자산 금액
- 총 저축액
- 은퇴 시점 자산
- 평균 수명까지의 자산 추이

#### 기능 1-1: 은퇴 자금 목표 계산 (신규 추가)

**기능 설명**:
은퇴 후 생활비와 의료비를 지속적으로 충당하기 위해 필요한 목표 자산을 계산하고, 다양한 저축 금액과 수익률 조합의 추이를 확인할 수 있습니다.

**입력**:
- 은퇴 후 월 생활비
- 은퇴 후 월 의료비
- 매달 저축 금액 (슬라이더로 추이 확인)
- 연간 수익률 (슬라이더로 추이 확인)
- 인플레이션율

**계산 원리**:
- **4% 현금화율 기준**: 은퇴 자산의 4%를 매년 인출하여 생활비로 사용하는 방식
- 목표 자산 = (은퇴 시점 연간 필요 금액) / 0.04
- 예상 자산 = 현재 자산의 미래가치 + 매달 저축의 미래가치 (복리 계산)

**출력**:
- 목표 자산
- 예상 자산
- 여유/부족 자산
- 저축 금액 vs 수익률 관계 그래프 (인터랙티브)
  - 초록색 영역: 목표 달성 가능한 조합
  - 빨간색 점선: 목표 달성 어려운 조합
  - 별표: 현재 선택한 값
- 최적 조합 제안 (수익률별 최소 저축 금액)

#### 기능 2: 재정 건전성 등급

**등급 기준**:

| 등급 | 기준          | 설명                  | 출처                    |
| ---- | ------------- | --------------------- | ----------------------- |
| A    | 저축률 > 30%  | 매우 건강한 재정 상태 | 금융감독원 가계금융조사 |
| B    | 저축률 20-30% | 건강한 재정 상태      | 금융감독원 가계금융조사 |
| C    | 저축률 10-20% | 보통 재정 상태        | 금융감독원 가계금융조사 |
| D    | 저축률 5-10%  | 주의 필요             | 금융감독원 가계금융조사 |
| E    | 저축률 0-5%   | 위험                  | 금융감독원 가계금융조사 |
| F    | 저축률 < 0%   | 매우 위험 (적자)      | 금융감독원 가계금융조사 |

**출처 근거**:

- 금융감독원 가계금융조사 보고서의 건강한 가계 기준
- OECD 평균 저축률 (약 20%) 참고
- 한국 평균 저축률 (약 15%) 참고

**계산 로직**:

```python
def calculate_financial_health_grade(
    annual_salary: float,
    monthly_expense: float
) -> str:
    """
    재정 건전성 등급 계산

    Returns:
        str: A, B, C, D, E, F 중 하나
    """
    annual_expense = monthly_expense * 12
    annual_savings = annual_salary - annual_expense
    savings_rate = (annual_savings / annual_salary) * 100

    if savings_rate >= 30:
        return "A"
    elif savings_rate >= 20:
        return "B"
    elif savings_rate >= 10:
        return "C"
    elif savings_rate >= 5:
        return "D"
    elif savings_rate >= 0:
        return "E"
    else:
        return "F"
```

#### 기능 3: 시나리오별 비교

**시나리오 종류**:

1. 현재 패턴 유지
2. 지출 10% 감소
3. 지출 20% 감소
4. 연봉 5% 증가
5. 연봉 10% 증가
6. 지출 10% 감소 + 연봉 5% 증가

**비교 항목**:

- 5년 후 자산
- 10년 후 자산
- 총 저축액
- 저축률

### 3.2 미래 리스크 및 시나리오 경고

#### 기능 1: 소득 중단 생존 기간

**데이터 출처**:

- 계산 방법: 자산 ÷ 월 지출
- 비상금 권장 기준: 금융감독원 (6개월치 생활비)
- 일반 금융 조언: 3-6개월치 생활비 준비 권장

**계산 가정**:

- 소득이 완전히 중단됨
- 지출 패턴 유지
- 자산 감소만 고려 (투자 수익 미고려)

**계산 로직**:

```python
def calculate_survival_months(
    total_assets: float,
    monthly_expense: float
) -> int:
    """
    소득 중단 시 생존 가능 기간 계산

    Returns:
        int: 생존 가능 월수
    """
    if monthly_expense <= 0:
        return float('inf')

    survival_months = int(total_assets / monthly_expense)
    return max(0, survival_months)
```

#### 기능 2: 경제 위기 시나리오

**시나리오**:

- 자산 30% 하락
- 자산 50% 하락

**출처 및 근거**:

- 2008 금융위기: 주식 시장 약 50% 하락 (참고)
- 2020 코로나19: 주식 시장 약 30% 하락 (참고)
- 금융감독원 스트레스 테스트 기준

**계산 로직**:

```python
def calculate_crisis_survival(
    total_assets: float,
    monthly_expense: float,
    asset_decline_rate: float = 0.3
) -> int:
    """
    경제 위기 시 생존 가능 기간

    Args:
        asset_decline_rate: 자산 하락률 (0.3 = 30%)

    Returns:
        int: 생존 가능 월수
    """
    crisis_assets = total_assets * (1 - asset_decline_rate)
    return calculate_survival_months(crisis_assets, monthly_expense)
```

#### 기능 3: 은퇴 시나리오

**출처 및 근거**:

- 통계청 생명표: 기대여명
- 국민연금공단: 평균 기대여명 약 20년 (60세 기준)
- 가정: 은퇴 후 20년간 생활비 유지

**계산 로직**:

```python
def check_retirement_viability(
    total_assets: float,
    monthly_expense: float,
    retirement_age: int,
    current_age: int,
    years_after_retirement: int = 20
) -> dict:
    """
    은퇴 시 생활비 유지 가능 여부

    Returns:
        dict: {
            'viable': bool,
            'shortfall': float,  # 부족한 금액
            'required_assets': float  # 필요한 자산
        }
    """
    years_to_retirement = retirement_age - current_age
    total_months = years_after_retirement * 12
    required_assets = monthly_expense * total_months

    viable = total_assets >= required_assets
    shortfall = max(0, required_assets - total_assets)

    return {
        'viable': viable,
        'shortfall': shortfall,
        'required_assets': required_assets
    }
```

#### 기능 4: 위험도 점수

**점수 계산 요소**:

1. 저축률 (40점)
2. 부채 비율 (30점)
3. 비상금 충분도 (30점)

**계산 로직**:

```python
def calculate_risk_score(
    total_assets: float,
    total_debt: float,
    monthly_expense: float,
    annual_salary: float,
    monthly_expense_input: float
) -> int:
    """
    위험도 점수 계산 (0-100, 높을수록 위험)

    Returns:
        int: 위험도 점수
    """
    # 1. 저축률 점수 (40점)
    annual_expense = monthly_expense_input * 12
    savings_rate = (annual_salary - annual_expense) / annual_salary * 100
    savings_score = max(0, 40 - (30 - savings_rate) * 2) if savings_rate < 30 else 0

    # 2. 부채 비율 점수 (30점)
    debt_ratio = (total_debt / total_assets * 100) if total_assets > 0 else 100
    debt_score = min(30, debt_ratio / 3)

    # 3. 비상금 충분도 점수 (30점)
    emergency_fund_months = total_assets / monthly_expense_input if monthly_expense_input > 0 else 0
    emergency_score = max(0, 30 - (6 - emergency_fund_months) * 5) if emergency_fund_months < 6 else 0

    total_score = savings_score + debt_score + emergency_score
    return min(100, int(total_score))
```

---

## 4. 입력 검증 상세

### 4.1 검증 규칙

```python
def validate_inputs(
    current_age: int,
    retirement_age: int,
    salary: float,
    monthly_expense: float,
    total_assets: float,
    total_debt: float
) -> tuple[bool, list]:
    """
    입력 검증

    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    warnings = []

    # 필수 입력 확인
    if current_age is None or current_age <= 0:
        errors.append("현재 나이를 입력해주세요")

    if retirement_age is None or retirement_age <= current_age:
        errors.append("은퇴 나이는 현재 나이보다 커야 합니다")

    if salary is None or salary < 0:
        errors.append("연봉을 입력해주세요")

    if monthly_expense is None or monthly_expense < 0:
        errors.append("월 지출을 입력해주세요")

    if total_assets is None or total_assets < 0:
        errors.append("자산을 입력해주세요")

    if total_debt is None or total_debt < 0:
        errors.append("부채를 입력해주세요")

    # 논리적 검증 (경고)
    if monthly_expense > salary / 12:
        warnings.append("⚠️ 월 지출이 월 소득보다 큽니다")

    if total_debt > total_assets:
        warnings.append("⚠️ 부채가 자산보다 큽니다. 순자산이 음수입니다")

    return len(errors) == 0, errors, warnings
```

---

## 5. 시각화 설계

### 5.1 나이별 자산 변화 그래프

**주요 특징**:
- X축: 나이 (세) - 연도가 아닌 나이로 표시하여 더 직관적
- 은퇴 시점을 수직선으로 표시
- 은퇴 전: 파란색 선 (자산 증가)
- 은퇴 후: 빨간색 선 (자산 감소)
- 평균 수명(83세)까지 표시

### 5.2 연도별 자산 변화 그래프 (구버전)

```python
import plotly.graph_objects as go

def create_asset_timeline_chart(years: list, assets: list) -> go.Figure:
    """
    연도별 자산 변화 라인 차트
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years,
        y=assets,
        mode='lines+markers',
        name='예상 자산',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title="연도별 자산 변화 추이",
        xaxis_title="연도",
        yaxis_title="자산 (만원)",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )

    return fig
```

### 5.2 시나리오 비교 그래프

```python
def create_scenario_comparison_chart(
    scenarios: list,
    base_data: dict
) -> go.Figure:
    """
    여러 시나리오 비교 그래프
    """
    fig = go.Figure()

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    for i, scenario in enumerate(scenarios):
        scenario_data = calculate_scenario(scenario, base_data)
        fig.add_trace(go.Scatter(
            x=scenario_data['years'],
            y=scenario_data['assets'],
            mode='lines+markers',
            name=scenario,
            line=dict(color=colors[i % len(colors)], width=2)
        ))

    fig.update_layout(
        title="시나리오별 자산 변화 비교",
        xaxis_title="연도",
        yaxis_title="자산 (만원)",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )

    return fig
```

---

## 6. 상태 관리

### 6.1 세션 상태 구조

각 페이지별로 독립적인 계산 상태를 유지하되, 입력 데이터는 공유:

```python
# shared/session_manager.py

def init_session_state():
    """세션 상태 초기화"""
    # 입력 데이터 (모든 페이지 공유)
    if 'current_age' not in st.session_state:
        st.session_state.current_age = 30
        st.session_state.retirement_age = 60
        st.session_state.salary = 5000
        st.session_state.salary_growth_rate = 3.0
        st.session_state.monthly_expense = 200
        st.session_state.total_assets = 1000
        st.session_state.total_debt = 0

    # 페이지별 계산 완료 상태
    if 'calculation_done_income' not in st.session_state:
        st.session_state.calculation_done_income = False
        st.session_state.calculation_done_risk = False
        st.session_state.calculation_done_comparison = False

    # 페이지별 결과 저장
    if 'results_income' not in st.session_state:
        st.session_state.results_income = None
        st.session_state.results_risk = None
        st.session_state.results_comparison = None

def get_shared_inputs():
    """공유 입력 데이터 반환"""
    return {
        'current_age': st.session_state.current_age,
        'retirement_age': st.session_state.retirement_age,
        'salary': st.session_state.salary,
        'salary_growth_rate': st.session_state.salary_growth_rate,
        'monthly_expense': st.session_state.monthly_expense,
        'total_assets': st.session_state.total_assets,
        'total_debt': st.session_state.total_debt
    }
```

### 6.2 페이지 간 데이터 공유

입력 폼 컴포넌트가 세션 상태를 업데이트하므로, 한 페이지에서 입력한 데이터가 다른 페이지에서도 사용 가능:

```python
# pages/1_소득_지출_분석.py에서 입력
inputs = render_input_form()  # 세션 상태 업데이트

# pages/2_리스크_시나리오.py에서 동일한 데이터 사용
inputs = render_input_form()  # 이미 입력된 값이 자동으로 표시됨
```

---

## 7. 에러 처리

### 7.1 에러 처리 전략

```python
def safe_calculate(func, *args, **kwargs):
    """안전한 계산 래퍼"""
    try:
        return func(*args, **kwargs)
    except ZeroDivisionError:
        st.error("계산 중 0으로 나누기 오류가 발생했습니다. 입력값을 확인해주세요.")
        return None
    except ValueError as e:
        st.error(f"입력값 오류: {str(e)}")
        return None
    except Exception as e:
        st.error(f"예상치 못한 오류가 발생했습니다: {str(e)}")
        st.info("문제가 지속되면 피드백을 보내주세요.")
        return None
```

---

## 8. 성능 최적화

### 8.1 계산 최적화

- 계산 결과 캐싱 (같은 입력 시 재계산 방지)
- 그래프 렌더링 최적화 (필요 시에만)
- 대용량 데이터 처리 시 샘플링

```python
@st.cache_data
def cached_calculation(inputs_hash: str, inputs: dict):
    """계산 결과 캐싱"""
    return perform_calculations(inputs)
```

---

## 9. 테스트 계획

### 9.1 단위 테스트

```python
# tests/test_calculations.py

def test_calculate_future_assets():
    assets = calculate_future_assets(
        current_assets=1000,
        annual_salary=5000,
        monthly_expense=200,
        salary_growth_rate=3.0,
        years=10
    )
    assert len(assets) == 11  # 0년부터 10년
    assert assets[0] == 1000
    assert assets[-1] > assets[0]  # 자산 증가 확인

def test_calculate_financial_health_grade():
    assert calculate_financial_health_grade(5000, 200) == "B"  # 저축률 20%
    assert calculate_financial_health_grade(5000, 350) == "F"  # 적자
```

### 9.2 통합 테스트

- 전체 워크플로우 테스트
- UI 요소 렌더링 테스트
- 에러 처리 테스트

---

## 10. 배포 계획

### 10.1 Streamlit Cloud 배포

1. **GitHub 저장소 생성**
2. **requirements.txt 작성**
3. **Streamlit Cloud 연결**
4. **환경 변수 설정** (필요 시)
5. **배포 및 테스트**

### 10.2 requirements.txt

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
python-dotenv>=1.0.0
```

---

## 11. 개발 일정

### Week 1-2: 기본 구조 및 입력 폼

- 파일 구조 설정
- 입력 폼 UI 구현
- 입력 검증 로직

### Week 3-4: 계산 로직 구현

- 자산 시뮬레이션 계산
- 리스크 계산
- 시나리오 비교

### Week 5: 시각화 및 UI 완성

- 그래프 생성
- 인사이트 텍스트 생성
- 결과 페이지 완성

### Week 6: 테스트 및 배포

- 테스트 수행
- 버그 수정
- Streamlit Cloud 배포
- 문서화

---

## 12. 데이터 출처 및 인사이트 근거

### 12.1 데이터 출처 표시 원칙

**필수 표시 사항**:

1. 계산에 사용된 가정 명시
2. 데이터 출처 표시
3. 제한사항 및 주의사항
4. 면책 조항

**표시 위치**:

- 각 결과 섹션 하단
- 별도 "데이터 출처" 섹션 (확장 가능)
- 다운로드 데이터에 포함

**참고**: 상세한 데이터 출처는 `docs/data_sources.md` 문서를 참조하세요.

### 12.2 주요 데이터 출처

| 데이터 타입      | Phase 1 출처                         | Phase 2 출처          |
| ---------------- | ------------------------------------ | --------------------- |
| 인플레이션       | 기본값 2.5% (한국은행 최근 3년 평균) | 한국은행 API (실시간) |
| 재정 건전성 기준 | 금융감독원 가계금융조사              | 동일                  |
| 비상금 기준      | 금융감독원 (6개월치 생활비)          | 동일                  |
| 연봉 증가율      | 사용자 입력 (통계청 평균 참고)       | 통계청 API (참고)     |
| 은퇴 기대여명    | 통계청 생명표 (20년 가정)            | 통계청 API            |

### 12.3 계산 가정 표시

```python
# 각 결과 페이지에 추가
st.markdown("---")
st.caption("💡 계산 가정: 인플레이션 미반영, 투자 수익 미고려")
st.caption("📚 출처: 금융감독원 가계금융조사, 한국은행 경제통계시스템")
st.caption("⚠️ 주의: 이 결과는 가정에 기반한 시뮬레이션입니다")
```

---

## 13. 인사이트 텍스트 생성

### 13.1 텍스트 생성 로직

```python
def generate_insight_text(
    future_assets_10y: float,
    current_assets: float,
    monthly_savings: float,
    financial_grade: str
) -> str:
    """
    사용자 친화적인 인사이트 텍스트 생성
    """
    insights = []

    # 자산 증가 인사이트
    asset_growth = future_assets_10y - current_assets
    if asset_growth > 0:
        insights.append(
            f"현재 소비 패턴을 유지하면 10년 후 약 {format_number(future_assets_10y)}만원이 됩니다. "
            f"이는 현재보다 약 {format_number(asset_growth)}만원 증가한 금액입니다."
        )
    else:
        insights.append(
            f"현재 소비 패턴을 유지하면 10년 후 자산이 {format_number(abs(asset_growth))}만원 감소합니다. "
            f"소비 패턴을 조정할 필요가 있습니다."
        )

    # 저축 인사이트
    if monthly_savings > 0:
        insights.append(
            f"현재 월 저축 가능액은 약 {format_number(monthly_savings)}만원입니다. "
            f"이를 투자하면 더 빠르게 자산을 늘릴 수 있습니다."
        )
    else:
        insights.append(
            f"현재 월 지출이 소득보다 큽니다. 지출을 줄이거나 소득을 늘려야 합니다."
        )

    # 등급별 조언
    grade_advice = {
        "A": "매우 건강한 재정 상태입니다! 현재 패턴을 유지하시면 됩니다.",
        "B": "건강한 재정 상태입니다. 투자를 고려해보세요.",
        "C": "보통 재정 상태입니다. 저축률을 조금 더 늘리면 좋겠습니다.",
        "D": "주의가 필요합니다. 지출을 줄이거나 소득을 늘리는 방법을 고려해보세요.",
        "E": "위험한 재정 상태입니다. 긴급히 재정 계획을 수정해야 합니다.",
        "F": "매우 위험한 상태입니다. 전문가의 도움을 받는 것을 권장합니다."
    }
    insights.append(grade_advice.get(financial_grade, ""))

    # 출처 및 가정 추가
    insights.append(
        "\n\n💡 계산 근거: 금융감독원 가계금융조사 기준, 한국은행 경제통계시스템 참고"
    )
    insights.append(
        "⚠️ 주의: 인플레이션 및 투자 수익은 고려하지 않았습니다. 실제 결과는 다를 수 있습니다."
    )

    return "\n\n".join(insights)

def format_number(value: float) -> str:
    """숫자 포맷팅 (만원 단위)"""
    if value >= 10000:
        return f"{value/10000:.1f}억"
    else:
        return f"{int(value):,}"
```

### 12.2 시나리오별 인사이트

```python
def generate_scenario_insight(
    base_result: dict,
    scenario_result: dict,
    scenario_name: str
) -> str:
    """
    시나리오별 비교 인사이트
    """
    base_assets = base_result['assets_10y']
    scenario_assets = scenario_result['assets_10y']
    difference = scenario_assets - base_assets

    if difference > 0:
        return (
            f"💡 {scenario_name} 시나리오를 적용하면 10년 후 "
            f"{format_number(difference)}만원 더 모을 수 있습니다. "
            f"이는 현재 자산의 약 {difference/base_result['current_assets']*100:.1f}%에 해당합니다."
        )
    else:
        return (
            f"⚠️ {scenario_name} 시나리오를 적용하면 10년 후 "
            f"{format_number(abs(difference))}만원이 줄어듭니다."
        )
```

## 14. 샘플 데이터 기능

### 13.1 샘플 시나리오 정의

```python
SAMPLE_SCENARIOS = {
    "신입 직장인": {
        'current_age': 25,
        'retirement_age': 60,
        'salary': 3000,
        'salary_growth_rate': 5.0,
        'monthly_expense': 150,
        'annual_fixed_expense': 200,
        'total_assets': 500,
        'total_debt': 0,
        'bonus': 0
    },
    "중년 직장인": {
        'current_age': 40,
        'retirement_age': 60,
        'salary': 6000,
        'salary_growth_rate': 3.0,
        'monthly_expense': 300,
        'annual_fixed_expense': 500,
        'total_assets': 5000,
        'total_debt': 2000,
        'bonus': 500
    },
    "은퇴 준비 중": {
        'current_age': 55,
        'retirement_age': 60,
        'salary': 8000,
        'salary_growth_rate': 2.0,
        'monthly_expense': 400,
        'annual_fixed_expense': 1000,
        'total_assets': 30000,
        'total_debt': 5000,
        'bonus': 1000
    }
}
```

### 13.2 샘플 데이터 적용 함수

```python
def apply_sample_data(scenario_name: str):
    """샘플 데이터를 세션 상태에 적용"""
    if scenario_name in SAMPLE_SCENARIOS:
        sample = SAMPLE_SCENARIOS[scenario_name]
        for key, value in sample.items():
            st.session_state[key] = value
        st.session_state['sample_applied'] = scenario_name
        st.success(f"'{scenario_name}' 시나리오 데이터가 적용되었습니다!")
        st.rerun()
```

## 15. 다운로드 기능

### 14.1 결과 다운로드

```python
def create_download_data(results: dict, user_inputs: dict) -> dict:
    """다운로드용 데이터 생성"""
    return {
        '입력 데이터': user_inputs,
        '계산 결과': {
            '10년 후 예상 자산': results['assets_10y'],
            '재정 건전성 등급': results['financial_grade'],
            '월 저축 가능액': results['monthly_savings'],
            '위험도 점수': results['risk_score']
        },
        '시나리오 비교': results['scenario_comparison'],
        '계산 일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

# 다운로드 버튼
if st.session_state.calculation_done:
    download_data = create_download_data(
        st.session_state.results,
        st.session_state.user_inputs
    )

    # JSON 다운로드
    json_str = json.dumps(download_data, ensure_ascii=False, indent=2)
    st.download_button(
        label="📥 결과 다운로드 (JSON)",
        data=json_str,
        file_name=f"finance_simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

    # CSV 다운로드 (시나리오 비교)
    csv_data = st.session_state.results['scenario_comparison'].to_csv(index=False)
    st.download_button(
        label="📊 시나리오 비교 다운로드 (CSV)",
        data=csv_data,
        file_name=f"scenario_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
```

## 16. 다음 단계 (Phase 2 준비)

- 사용자 피드백 수집
- 추가 기능 우선순위 결정
- Notion 연동 검토
- API 연동 (인플레이션, 환율)

---

## 17. 정의되지 않은 함수 및 로직

### 16.1 누락된 함수 목록

다음 함수들은 페이지 코드에서 호출되지만 구현이 명확히 정의되지 않았습니다:

1. **`calculate_scenario(scenario, base_data)`** - 시나리오별 계산
2. **`create_comparison_table(scenarios, base_data)`** - 비교 테이블 생성
3. **`perform_calculations(inputs)`** - 전체 계산 수행 (페이지별로 분리 필요)
4. **`validate_inputs()`** - 반환값 사용 방식 불일치 (튜플 vs 단일 값)
5. **샘플 데이터 UI** - 사이드바에 표시하는 컴포넌트
6. **피드백 수집 UI** - 실제 구현 코드

### 16.2 불명확한 부분

1. **페이지별 결과 데이터 구조** - 각 페이지의 계산 결과 dict 구조
2. **페이지 초기화 시점** - 세션 상태 초기화 타이밍
3. **에러 처리 사용자 안내** - 계산 실패 시 UI 표시 방법
4. **시나리오 이름 파싱** - "지출 -10%" 같은 문자열 파싱 로직

**참고**: 상세한 구현은 `docs/phase1_missing_functions.md` 문서를 참조하세요.

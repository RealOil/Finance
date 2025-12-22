# 모바일 최적화

## 현재 요구사항 문서의 관련 내용

### 기존 명시 사항

- 반응형 디자인 (모바일 최소 지원) (3.2 사용성)
- Termux에서 실행 후 Streamlit 접근 가능 (5.1.1 배포 옵션)

---

## 추가 확인 필요 사항

### 1. 모바일 UI 레이아웃

**문제 상황**:

- 데스크톱 중심 설계로 모바일에서 사용 불편
- 입력 필드가 많아 스크롤이 길어짐
- 그래프가 모바일에서 보기 어려움

**제안**:

#### 반응형 레이아웃

**옵션 A: 모바일 우선 설계 (추천)**

- 모바일 화면에 최적화
- 데스크톱에서는 여유 공간 활용
- Streamlit의 반응형 기능 활용

**옵션 B: 모바일 전용 버전**

- 별도의 모바일 최적화 페이지
- 필수 기능만 포함
- 간소화된 UI

#### 구현 방법

```python
import streamlit as st

# 화면 크기 감지 (JavaScript 필요)
st.markdown("""
<script>
    function getScreenWidth() {
        return window.innerWidth;
    }
    window.screenWidth = getScreenWidth();
</script>
""", unsafe_allow_html=True)

# 모바일 감지 (User Agent 또는 화면 크기)
is_mobile = st.session_state.get('is_mobile', False)

if is_mobile:
    # 모바일 레이아웃
    st.markdown("### 📱 모바일 모드")

    # 사이드바 대신 메인 영역에 입력
    with st.expander("기본 정보 입력", expanded=True):
        current_age = st.number_input("현재 나이", min_value=0, max_value=150)
        retirement_age = st.number_input("은퇴 나이", min_value=0, max_value=100)

    with st.expander("소득 정보"):
        salary = st.number_input("연봉 (만원)", min_value=0)

    # 그래프는 작게 표시
    st.plotly_chart(fig, use_container_width=True, height=300)
else:
    # 데스크톱 레이아웃
    col1, col2 = st.columns(2)
    with col1:
        # 입력 폼
    with col2:
        # 미리보기
```

---

### 2. 터치 최적화

**문제 상황**:

- 버튼이 너무 작아 터치하기 어려움
- 입력 필드가 작아 입력 불편
- 스와이프 제스처 미지원

**제안**:

#### 터치 친화적 UI

**버튼 크기**:

- 최소 44x44 픽셀 (Apple 가이드라인)
- 충분한 여백
- 명확한 시각적 피드백

**입력 필드**:

- 충분한 높이 (최소 40px)
- 큰 폰트 크기
- 자동 포커스 (선택적)

**구현 방법**:

```python
# Streamlit에서 버튼 스타일 커스터마이징
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 18px;
        border-radius: 10px;
    }

    .stNumberInput > div > div > input {
        font-size: 18px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 큰 버튼
st.button("계산하기", use_container_width=True)
```

---

### 3. 모바일 데이터 입력 최적화

**문제 상황**:

- 긴 숫자 입력이 불편
- 천 단위 구분 기호 입력 어려움
- 복사-붙여넣기 불편

**제안**:

#### 입력 최적화

**숫자 키패드**:

- 모바일에서 숫자 입력 시 숫자 키패드 자동 표시
- HTML5 `input type="number"` 활용

**자동 포맷팅**:

- 입력 중 자동으로 천 단위 구분
- "1,000만원" 형식으로 표시

**구현 방법**:

```python
# 숫자 입력 필드 (모바일 키패드 최적화)
st.number_input(
    "연봉 (만원)",
    min_value=0,
    step=100,  # 100만원 단위
    format="%d"  # 정수만
)

# 또는 텍스트 입력 + 자동 포맷팅
salary_text = st.text_input(
    "연봉 (만원)",
    type="default",
    help="숫자만 입력하세요. 예: 5000"
)

# 자동 포맷팅
if salary_text:
    try:
        salary = int(salary_text.replace(',', ''))
        st.caption(f"입력된 금액: {salary:,}만원")
    except ValueError:
        st.error("숫자만 입력해주세요")
```

---

### 4. 모바일 그래프 최적화

**문제 상황**:

- 그래프가 작아서 보기 어려움
- 인터랙션 (줌, 팬)이 터치에서 불편
- 여러 그래프를 한 화면에 표시하기 어려움

**제안**:

#### 그래프 최적화

**옵션 A: 전체 화면 그래프 (추천)**

- 그래프 클릭 시 전체 화면으로 확대
- 모바일에서 스와이프로 탐색

**옵션 B: 간소화된 그래프**

- 모바일에서는 핵심 정보만 표시
- 상세 그래프는 데스크톱에서만

**구현 방법**:

```python
import plotly.graph_objects as go

# Plotly 그래프 생성
fig = go.Figure(...)

# 모바일 최적화 설정
fig.update_layout(
    height=400 if is_mobile else 600,
    font=dict(size=14 if is_mobile else 12),
    margin=dict(l=20, r=20, t=20, b=20)
)

# 모바일에서 전체 화면 버튼 추가
if is_mobile:
    st.markdown("💡 그래프를 탭하면 전체 화면으로 볼 수 있습니다")

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['pan2d', 'lasso2d']  # 모바일에서 불필요한 버튼 제거
    }
)
```

---

### 5. 모바일 네비게이션

**문제 상황**:

- 여러 섹션 간 이동이 불편
- 하단 네비게이션 바 없음
- 뒤로 가기 버튼 동작 불명확

**제안**:

#### 네비게이션 개선

**옵션 A: 탭 네비게이션**

- 상단에 탭으로 섹션 구분
- 모바일에서 스와이프로 이동

**옵션 B: 하단 네비게이션**

- 주요 기능을 하단에 고정
- 항상 접근 가능

**구현 방법**:

```python
# Streamlit 탭 사용
tab1, tab2, tab3 = st.tabs(["📊 분석", "💰 시뮬레이션", "📈 결과"])

with tab1:
    st.markdown("### 소득 및 지출 분석")
    # 분석 내용

with tab2:
    st.markdown("### 미래 시뮬레이션")
    # 시뮬레이션 내용

with tab3:
    st.markdown("### 결과 및 인사이트")
    # 결과 내용
```

---

### 6. 모바일 성능 최적화

**문제 상황**:

- 모바일에서 로딩이 느림
- 그래프 렌더링 지연
- 배터리 소모

**제안**:

#### 성능 최적화

**레이지 로딩**:

- 초기에는 필수 기능만 로드
- 그래프는 필요 시에만 렌더링

**데이터 최적화**:

- 모바일에서는 데이터 포인트 수 제한
- 그래프 해상도 조정

**구현 방법**:

```python
# 조건부 로딩
if st.session_state.get('show_graph', False):
    # 그래프 렌더링 (무거운 작업)
    fig = create_complex_graph()
    st.plotly_chart(fig)
else:
    # 간단한 요약만 표시
    st.metric("예상 자산", "5,000만원")
    if st.button("상세 그래프 보기"):
        st.session_state.show_graph = True
        st.rerun()
```

---

## 구현 우선순위

### Phase 1 (필수)

1. ✅ 기본 반응형 레이아웃 (Streamlit 기본 기능 활용)
2. ✅ 터치 친화적 버튼 크기
3. ✅ 모바일 숫자 키패드 (input type="number")
4. ✅ 그래프 반응형 크기 조정

### Phase 2 (권장)

5. ⚠️ 모바일 전용 레이아웃
6. ⚠️ 탭 네비게이션
7. ⚠️ 전체 화면 그래프
8. ⚠️ 성능 최적화 (레이지 로딩)

---

## 테스트 방법

### 모바일 테스트

1. **실제 기기 테스트**: iOS, Android 실제 기기에서 테스트
2. **브라우저 개발자 도구**: Chrome DevTools 모바일 시뮬레이션
3. **다양한 화면 크기**: iPhone SE, iPhone 14 Pro, Galaxy S23 등

### 테스트 체크리스트

- [ ] 모든 입력 필드가 터치하기 쉬운가?
- [ ] 버튼이 충분히 큰가?
- [ ] 그래프가 모바일에서 잘 보이는가?
- [ ] 스크롤이 부드러운가?
- [ ] 로딩 시간이 적절한가?

---

## 사용자 경험 원칙

1. **터치 우선**: 모든 인터랙션은 터치로 쉽게
2. **간결함**: 모바일에서는 핵심 기능만 강조
3. **빠른 로딩**: 모바일 데이터 절약 고려
4. **일관성**: 데스크톱과 모바일 간 일관된 경험

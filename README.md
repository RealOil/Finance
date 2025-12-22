# Financial Freedom Simulation Tool

재정 자유도 시뮬레이션 도구 - Phase 1 MVP

## 프로젝트 소개

이 도구는 사용자의 소득, 지출, 자산 정보를 기반으로 미래 재정 상황을 시뮬레이션하고, 다양한 리스크 시나리오를 분석하여 재정 건전성을 평가합니다.

## 주요 기능

### Phase 1 (현재)

1. **소득 및 지출 분석**
   - 10년 후 예상 자산 추정
   - 재정 건전성 등급 평가
   - 월 저축 가능액 계산

2. **리스크 시나리오 분석**
   - 소득 중단 시 생존 가능 기간
   - 경제 위기 시나리오 (자산 하락)
   - 은퇴 시 생활비 유지 가능 여부
   - 위험도 점수 계산

3. **시나리오 비교**
   - 다양한 시나리오별 자산 변화 비교
   - 지출 감소, 연봉 증가 등 시나리오 시뮬레이션

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd Finance
```

### 2. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
streamlit run app.py
```

브라우저에서 자동으로 열리며, 기본 주소는 `http://localhost:8501`입니다.

## 프로젝트 구조

```
finance-simulator/
├── app.py                 # 메인 홈 페이지
├── pages/                 # 기능별 페이지
│   ├── 1_소득_지출_분석.py
│   ├── 2_리스크_시나리오.py
│   └── 3_시나리오_비교.py
├── modules/               # 계산 및 유틸리티 모듈
│   ├── calculations.py
│   ├── validators.py
│   ├── formatters.py
│   └── visualizations.py
├── shared/                # 공통 모듈
│   ├── input_form.py
│   └── session_manager.py
├── data/                  # 데이터 및 기본값
│   └── defaults.py
├── config/                # 설정
│   └── constants.py
├── plan/                  # 계획 문서
├── tests/                 # 테스트 파일
└── docs/                  # 문서
```

## 사용 방법

1. 사이드바에서 재정 정보 입력
   - 기본 정보 (나이, 은퇴 나이)
   - 소득 정보 (연봉, 연봉 증가율)
   - 소비 정보 (월 지출)
   - 자산 및 부채

2. "계산하기" 버튼 클릭

3. 결과 확인
   - 각 페이지에서 계산 결과 및 인사이트 확인
   - 그래프 및 시각화 자료 확인

## 데이터 출처

모든 데이터 출처 및 계산 근거는 `docs/data_sources.md`를 참조하세요.

## 면책 조항

이 도구는 교육 및 시뮬레이션 목적으로만 제공됩니다.

- 금융 조언이 아닙니다
- 투자 권유가 아닙니다
- 실제 재정 결정에 대한 책임을 지지 않습니다
- 전문가의 조언을 받는 것을 권장합니다

## 개발 상태

**Phase 1 (MVP)**: 개발 중

- [x] 프로젝트 구조 설정
- [ ] 핵심 기능 구현
- [ ] 테스트
- [ ] 배포

## 라이선스

[라이선스 정보 추가]

## 기여

[기여 가이드 추가]


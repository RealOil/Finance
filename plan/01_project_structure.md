# 작업 1.1: 프로젝트 기본 구조 설정

## 작업 정보

- **작업 ID**: 01_project_structure
- **우선순위**: 높음 (필수)
- **예상 시간**: 0.5일
- **시작 시간**: 2025-12-21 (타임스탬프는 실제 구현 시 확인)

---

## 작업 목표

프로젝트의 기본 디렉토리 구조를 생성하고, 필수 설정 파일들을 작성합니다.

---

## 작업 내용

### 1. 디렉토리 구조 생성

다음 디렉토리들을 생성합니다:

```
finance-simulator/
├── app.py
├── pages/
│   ├── 1_소득_지출_분석.py
│   ├── 2_리스크_시나리오.py
│   └── 3_시나리오_비교.py
├── modules/
│   ├── calculations.py
│   ├── validators.py
│   ├── formatters.py
│   └── visualizations.py
├── shared/
│   ├── input_form.py
│   └── session_manager.py
├── data/
│   └── defaults.py
├── config/
│   └── constants.py
├── plan/              # 계획 문서
├── tests/             # 테스트 파일
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### 2. requirements.txt 작성

필수 패키지 목록:

- streamlit>=1.28.0
- pandas>=2.0.0
- plotly>=5.17.0
- python-dotenv>=1.0.0

### 3. .gitignore 작성

Python 프로젝트 표준 .gitignore:
- __pycache__/
- *.py[cod]
- .env
- .venv/
- venv/
- *.log
- .streamlit/

### 4. README.md 작성

포함 내용:
- 프로젝트 소개
- 설치 방법
- 실행 방법
- 주요 기능
- 라이선스

### 5. .env.example 작성

환경 변수 예시 (필요 시):
- API 키 등 (Phase 1에서는 선택적)

---

## 구현 체크리스트

- [x] 디렉토리 구조 생성 (2025-12-21 22:53:15)
- [x] requirements.txt 작성 (2025-12-21 22:53:15)
- [x] .gitignore 작성 (2025-12-21 22:53:15)
- [x] README.md 작성 (2025-12-21 22:53:15)
- [x] .env.example 작성 (선택적, .gitignore에 의해 차단됨)
- [x] 각 디렉토리에 __init__.py 파일 생성 (2025-12-21 22:54:15)

---

## 테스트 계획

### 테스트 항목

1. **디렉토리 존재 확인**
   - 모든 디렉토리가 존재하는지 확인
   - 파일이 올바른 위치에 있는지 확인

2. **requirements.txt 검증**
   - 패키지 이름이 올바른지 확인
   - 버전 지정이 적절한지 확인

3. **.gitignore 검증**
   - 필수 항목이 포함되어 있는지 확인

4. **README.md 검증**
   - 필수 섹션이 포함되어 있는지 확인

---

## 예상 결과

- 프로젝트 디렉토리 구조가 완성됨
- 필수 설정 파일들이 작성됨
- 다음 작업(세션 상태 관리 모듈)을 시작할 수 있는 상태

---

## 다음 작업

작업 1.2: 세션 상태 관리 모듈 구현


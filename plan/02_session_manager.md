# 작업 1.2: 세션 상태 관리 모듈

## 작업 정보

- **작업 ID**: 02_session_manager
- **우선순위**: 높음 (필수)
- **예상 시간**: 0.5일
- **계획 작성 시간**: 2025-12-21 22:56:30
- **구현 시작 시간**: 2025-12-21 23:00:47
- **구현 완료 시간**: 2025-12-21 23:01:00
- **테스트 완료 시간**: 2025-12-21 23:02:30

---

## 작업 목표

Streamlit 세션 상태를 관리하는 모듈을 구현하여 모든 페이지에서 공유할 수 있는 입력 데이터와 계산 결과를 관리합니다.

---

## 작업 내용

### 1. 세션 상태 초기화 함수

**함수**: `init_session_state()`

**기능**:
- 입력 데이터 초기화
  - current_age (기본값: 30)
  - retirement_age (기본값: 60)
  - salary (기본값: 5000)
  - salary_growth_rate (기본값: 3.0)
  - bonus (기본값: 0)
  - monthly_expense (기본값: 200)
  - annual_fixed_expense (기본값: 0)
  - total_assets (기본값: 1000)
  - total_debt (기본값: 0)

- 페이지별 계산 완료 상태 초기화
  - calculation_done_income (기본값: False)
  - calculation_done_risk (기본값: False)
  - calculation_done_comparison (기본값: False)

- 페이지별 결과 저장소 초기화
  - results_income (기본값: None)
  - results_risk (기본값: None)
  - results_comparison (기본값: None)

### 2. 공유 입력 데이터 반환 함수

**함수**: `get_shared_inputs()`

**기능**:
- 세션 상태에서 입력 데이터를 딕셔너리로 반환
- 모든 페이지에서 동일한 입력 데이터 사용 가능

**반환 형식**:
```python
{
    'current_age': int,
    'retirement_age': int,
    'salary': float,
    'salary_growth_rate': float,
    'bonus': float,
    'monthly_expense': float,
    'annual_fixed_expense': float,
    'total_assets': float,
    'total_debt': float
}
```

---

## 구현 체크리스트

- [x] `shared/session_manager.py` 파일 생성 (2025-12-21 22:57:00)
- [x] `init_session_state()` 함수 구현 (2025-12-21 22:57:15)
- [x] `get_shared_inputs()` 함수 구현 (2025-12-21 22:57:30)
- [x] 타입 힌트 추가
- [x] docstring 작성

---

## 테스트 계획

### 테스트 항목

1. **세션 상태 초기화 테스트**
   - 모든 필수 키가 세션 상태에 존재하는지 확인
   - 기본값이 올바르게 설정되었는지 확인

2. **공유 입력 데이터 반환 테스트**
   - `get_shared_inputs()` 함수가 올바른 딕셔너리를 반환하는지 확인
   - 세션 상태 변경 시 반환값이 업데이트되는지 확인

3. **타입 검증**
   - 반환값의 타입이 올바른지 확인

---

## 예상 결과

- 세션 상태 관리 모듈이 완성됨
- 모든 페이지에서 공유 입력 데이터를 사용할 수 있음
- 다음 작업(공통 입력 폼 컴포넌트)을 시작할 수 있는 상태

---

## 다음 작업

작업 1.3: 공통 입력 폼 컴포넌트 구현


# 작업 1.8: 데이터 포맷팅 모듈 구현

## 작업 정보

- **작업 ID**: 08_formatters
- **우선순위**: 중간
- **예상 시간**: 1일
- **계획 작성 시간**: 2025-12-21 23:31:20
- **구현 시작 시간**: 2025-12-21 23:31:31
- **구현 완료 시간**: 2025-12-21 23:32:00
- **테스트 완료 시간**: 2025-12-21 23:32:30

---

## 작업 목표

숫자 포맷팅과 인사이트 텍스트 생성을 담당하는 모듈을 구현합니다.
사용자에게 보기 좋고 이해하기 쉬운 형식으로 데이터를 표시합니다.

---

## 작업 내용

### 1. 숫자 포맷팅 함수

**함수**: `format_currency(value: float, unit: str = "만원") -> str`

**기능**:
- 금액을 읽기 쉬운 형식으로 포맷팅
- 천 단위 구분 기호 추가
- 소수점 처리

**예시**:
- 5000 → "5,000만원"
- 12345.67 → "12,346만원" (반올림)
- 0 → "0만원"

**함수**: `format_percentage(value: float, decimals: int = 1) -> str`

**기능**:
- 퍼센트 값을 포맷팅
- 소수점 자릿수 지정

**예시**:
- 3.0 → "3.0%"
- 3.456 → "3.5%" (decimals=1)

**함수**: `format_number(value: float, decimals: int = 0) -> str`

**기능**:
- 일반 숫자 포맷팅
- 천 단위 구분 기호 추가

**예시**:
- 1234.56 → "1,235" (decimals=0)
- 1234.56 → "1,234.6" (decimals=1)

### 2. 인사이트 텍스트 생성 함수

**함수**: `generate_financial_health_insight(grade_result: Dict[str, Any]) -> str`

**기능**:
- 재정 건전성 등급에 따른 인사이트 텍스트 생성
- 등급별 맞춤 메시지 제공

**예시**:
- A+ 등급: "매우 건강한 재정 상태입니다. 현재 패턴을 유지하시면 안정적인 미래를 기대할 수 있습니다."
- D 등급: "재정 상태 개선이 필요합니다. 지출을 줄이고 저축을 늘리는 것을 권장합니다."

**함수**: `generate_risk_insight(risk_result: Dict[str, Any]) -> str`

**기능**:
- 위험도 점수에 따른 인사이트 텍스트 생성
- 위험도별 맞춤 메시지 제공

**함수**: `generate_future_assets_insight(future_assets_result: Dict[str, Any]) -> str`

**기능**:
- 미래 자산 추정 결과에 따른 인사이트 텍스트 생성
- 현재 자산과 비교하여 메시지 생성

**함수**: `generate_retirement_insight(retirement_result: Dict[str, Any]) -> str`

**기능**:
- 은퇴 시나리오 결과에 따른 인사이트 텍스트 생성
- 지속 가능 여부에 따른 메시지 생성

### 3. 상태별 메시지 생성 함수

**함수**: `get_status_message(status: str, category: str) -> str`

**기능**:
- 상태 코드에 따른 메시지 반환
- 카테고리별 맞춤 메시지

**상태 코드**:
- safe, warning, danger
- sustainable, warning, danger
- low, medium, high, critical

---

## 구현 체크리스트

- [x] `modules/formatters.py` 파일 생성 (2025-12-21 23:31:31)
- [x] `format_currency()` 함수 구현 (2025-12-21 23:31:45)
- [x] `format_percentage()` 함수 구현
- [x] `format_number()` 함수 구현
- [x] `generate_financial_health_insight()` 함수 구현 (2025-12-21 23:31:55)
- [x] `generate_risk_insight()` 함수 구현
- [x] `generate_future_assets_insight()` 함수 구현
- [x] `generate_retirement_insight()` 함수 구현
- [x] `get_status_message()` 함수 구현 (2025-12-21 23:32:00)
- [x] 타입 힌트 추가
- [x] docstring 작성

---

## 테스트 계획

### 테스트 항목

1. **숫자 포맷팅 테스트**
   - 금액 포맷팅
   - 퍼센트 포맷팅
   - 일반 숫자 포맷팅
   - 경계값 테스트 (0, 음수, 큰 수)

2. **인사이트 텍스트 생성 테스트**
   - 재정 건전성 인사이트
   - 위험도 인사이트
   - 미래 자산 인사이트
   - 은퇴 인사이트

3. **상태 메시지 테스트**
   - 각 상태별 메시지 확인

---

## 예상 결과

- 데이터 포맷팅 모듈이 완성됨
- 사용자 친화적인 형식으로 데이터 표시 가능
- 인사이트 텍스트 자동 생성 가능
- 다음 작업(시각화 모듈)을 시작할 수 있는 상태

---

## 다음 작업

작업 1.9: 시각화 모듈 구현


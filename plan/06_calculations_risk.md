# 작업 1.6: 리스크 계산 로직 구현

## 작업 정보

- **작업 ID**: 06_calculations_risk
- **우선순위**: 높음 (필수)
- **예상 시간**: 2일
- **계획 작성 시간**: 2025-12-21 23:22:44
- **구현 시작 시간**: 2025-12-21 23:22:55
- **구현 완료 시간**: 2025-12-21 23:23:31
- **테스트 완료 시간**: 2025-12-21 23:24:00

---

## 작업 목표

다양한 리스크 시나리오를 분석하는 계산 로직을 구현합니다.
소득 중단, 경제 위기, 은퇴 시나리오 등을 계산하고 위험도 점수를 산출합니다.

---

## 작업 내용

### 1. 소득 중단 생존 기간 계산 함수

**함수**: `calculate_income_interruption_survival(inputs: Dict[str, Any]) -> Dict[str, Any]`

**기능**:
- 소득이 완전히 중단되었을 때 자산으로 버틸 수 있는 기간 계산
- 월 지출 기준으로 계산

**계산 로직**:
```
순자산 = 총 자산 - 총 부채
월 지출 = 월 지출 + (연간 고정 지출 / 12)
생존 가능 개월 = 순자산 / 월 지출
```

**반환값**:
```python
{
    'survival_months': float,
    'survival_years': float,
    'net_assets': float,
    'monthly_expense': float,
    'status': str,  # 'safe', 'warning', 'danger'
    'recommendation': str
}
```

**등급 기준**:
- safe: 6개월 이상
- warning: 3-6개월
- danger: 3개월 미만

### 2. 경제 위기 시나리오 계산 함수

**함수**: `calculate_crisis_scenario(inputs: Dict[str, Any], asset_drop_rate: float = 30.0) -> Dict[str, Any]`

**기능**:
- 자산이 일정 비율 하락했을 때의 상황 계산
- 기본 하락률: 30% (코로나19 시나리오), 50% (금융위기 시나리오)

**계산 로직**:
```
위기 후 자산 = 현재 자산 × (1 - 하락률 / 100)
위기 후 순자산 = 위기 후 자산 - 총 부채
생존 가능 개월 = 위기 후 순자산 / 월 지출
```

**반환값**:
```python
{
    'asset_drop_rate': float,
    'assets_before': float,
    'assets_after': float,
    'net_assets_after': float,
    'survival_months': float,
    'status': str
}
```

### 3. 은퇴 시 생활비 유지 가능 여부 계산 함수

**함수**: `calculate_retirement_sustainability(inputs: Dict[str, Any]) -> Dict[str, Any]`

**기능**:
- 은퇴 시점의 예상 자산 계산
- 은퇴 후 월 생활비 유지 가능 기간 계산
- 은퇴 시 생활비 = 현재 월 지출 (인플레이션 반영)

**계산 로직**:
```
은퇴까지 남은 연수 = 은퇴 나이 - 현재 나이
은퇴 시점 예상 자산 = calculate_future_assets(inputs, years=은퇴까지 남은 연수)
은퇴 후 월 생활비 = 현재 월 지출 × (1 + 인플레이션)^은퇴까지 남은 연수
은퇴 후 생존 가능 개월 = 은퇴 시점 예상 자산 / 은퇴 후 월 생활비
```

**반환값**:
```python
{
    'years_to_retirement': int,
    'expected_assets_at_retirement': float,
    'monthly_expense_at_retirement': float,
    'survival_months': float,
    'survival_years': float,
    'life_expectancy_after_retirement': int,  # 기본값: 20년
    'is_sustainable': bool,
    'status': str,
    'recommendation': str
}
```

### 4. 위험도 점수 계산 함수

**함수**: `calculate_risk_score(inputs: Dict[str, Any]) -> Dict[str, Any]`

**기능**:
- 여러 리스크 요소를 종합하여 위험도 점수 계산 (0-100)
- 점수가 높을수록 위험

**점수 구성 요소**:
1. 소득 중단 생존 기간 (40점)
   - 6개월 이상: 0점
   - 3-6개월: 20점
   - 3개월 미만: 40점

2. 부채 비율 (30점)
   - 부채 비율 0%: 0점
   - 부채 비율 20%: 10점
   - 부채 비율 40%: 20점
   - 부채 비율 60% 이상: 30점

3. 소득 대비 지출 비율 (20점)
   - 지출 비율 < 50%: 0점
   - 지출 비율 50-70%: 10점
   - 지출 비율 70-90%: 20점
   - 지출 비율 90% 이상: 20점

4. 은퇴 준비도 (10점)
   - 은퇴 후 생존 가능 기간이 기대 수명보다 길면: 0점
   - 기대 수명의 50% 이상: 5점
   - 기대 수명의 50% 미만: 10점

**반환값**:
```python
{
    'total_score': int,  # 0-100
    'risk_level': str,  # 'low', 'medium', 'high', 'critical'
    'breakdown': {
        'income_interruption': int,
        'debt_ratio': int,
        'expense_ratio': int,
        'retirement_readiness': int
    },
    'recommendations': List[str]
}
```

---

## 구현 체크리스트

- [x] `calculate_income_interruption_survival()` 함수 구현 (2025-12-21 23:23:00)
- [x] `calculate_crisis_scenario()` 함수 구현 (2025-12-21 23:23:15)
- [x] `calculate_retirement_sustainability()` 함수 구현 (2025-12-21 23:23:25)
- [x] `calculate_risk_score()` 함수 구현 (2025-12-21 23:23:31)
- [x] 타입 힌트 추가
- [x] docstring 작성

---

## 테스트 계획

### 테스트 항목

1. **소득 중단 생존 기간 테스트**
   - 정상 케이스
   - 위험 케이스 (3개월 미만)
   - 안전 케이스 (6개월 이상)

2. **경제 위기 시나리오 테스트**
   - 30% 하락 시나리오
   - 50% 하락 시나리오
   - 위기 후 생존 가능 기간 계산

3. **은퇴 시나리오 테스트**
   - 은퇴 시점 자산 계산
   - 은퇴 후 생존 가능 기간 계산
   - 지속 가능 여부 판단

4. **위험도 점수 테스트**
   - 각 구성 요소별 점수 계산
   - 종합 점수 계산
   - 위험도 등급 산출

---

## 데이터 출처

- 비상금 기준: 6개월치 생활비 (금융감독원 권장)
- 경제 위기 하락률: 30% (코로나19), 50% (금융위기)
- 은퇴 후 기대 수명: 20년 (docs/data_sources.md)

---

## 예상 결과

- 리스크 계산 로직이 완성됨
- 다양한 리스크 시나리오 분석 가능
- 위험도 점수 산출 가능
- 다음 작업(시나리오 비교 계산 로직)을 시작할 수 있는 상태

---

## 다음 작업

작업 1.7: 시나리오 비교 계산 로직 구현


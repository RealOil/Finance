# 작업 1.7: 시나리오 비교 계산 로직 구현

## 작업 정보

- **작업 ID**: 07_calculations_scenario
- **우선순위**: 높음 (필수)
- **예상 시간**: 1.5일
- **계획 작성 시간**: 2025-12-21 23:27:19
- **구현 시작 시간**: 2025-12-21 23:27:30
- **구현 완료 시간**: 2025-12-21 23:27:48
- **테스트 완료 시간**: 2025-12-21 23:28:16

---

## 작업 목표

다양한 시나리오를 비교하는 계산 로직을 구현합니다.
지출 감소, 연봉 증가 등의 시나리오를 적용하여 미래 자산을 비교합니다.

---

## 작업 내용

### 1. 시나리오 파싱 함수

**함수**: `parse_scenario(scenario_string: str) -> Dict[str, Any]`

**기능**:
- 시나리오 문자열을 파싱하여 변경 사항 딕셔너리로 변환
- 지원 형식: "지출 10% 감소", "연봉 5% 증가", "지출 10% 감소 + 연봉 5% 증가"

**반환값**:
```python
{
    'expense_change': float,  # 지출 변화율 (%)
    'salary_change': float,   # 연봉 변화율 (%)
    'description': str        # 시나리오 설명
}
```

**예시**:
- "지출 10% 감소" → {'expense_change': -10, 'salary_change': 0, 'description': '지출 10% 감소'}
- "연봉 5% 증가" → {'expense_change': 0, 'salary_change': 5, 'description': '연봉 5% 증가'}
- "지출 10% 감소 + 연봉 5% 증가" → {'expense_change': -10, 'salary_change': 5, 'description': '지출 10% 감소 + 연봉 5% 증가'}

### 2. 시나리오 계산 함수

**함수**: `calculate_scenario(inputs: Dict[str, Any], scenario: Dict[str, Any], years: int = 10) -> Dict[str, Any]`

**기능**:
- 입력 데이터에 시나리오를 적용하여 미래 자산 계산
- 시나리오 변경사항을 입력 데이터에 반영
- `calculate_future_assets()` 함수를 재사용

**계산 로직**:
```
수정된 입력 = 원본 입력 복사
수정된 입력['monthly_expense'] = 원본 × (1 + expense_change / 100)
수정된 입력['salary'] = 원본 × (1 + salary_change / 100)
미래 자산 = calculate_future_assets(수정된 입력, years)
```

**반환값**:
```python
{
    'scenario': Dict[str, Any],  # 시나리오 정보
    'future_assets': float,       # 미래 자산
    'total_savings': float,       # 총 저축액
    'yearly_breakdown': List[Dict]  # 연도별 상세 내역
}
```

### 3. 여러 시나리오 비교 함수

**함수**: `compare_scenarios(inputs: Dict[str, Any], scenarios: List[str], years: int = 10) -> Dict[str, Any]`

**기능**:
- 여러 시나리오를 동시에 계산하여 비교
- 각 시나리오별 결과를 리스트로 반환

**반환값**:
```python
{
    'base_scenario': Dict[str, Any],  # 기본 시나리오 (현재 패턴 유지)
    'scenarios': List[Dict[str, Any]],  # 각 시나리오별 결과
    'comparison': {
        'best_scenario': str,      # 최고 자산 시나리오
        'worst_scenario': str,     # 최저 자산 시나리오
        'differences': Dict        # 시나리오별 차이
    }
}
```

### 4. 기본 시나리오 목록

**기본 제공 시나리오**:
1. "현재 패턴 유지" (기본)
2. "지출 10% 감소"
3. "지출 20% 감소"
4. "연봉 5% 증가"
5. "연봉 10% 증가"
6. "지출 10% 감소 + 연봉 5% 증가"

---

## 구현 체크리스트

- [x] `parse_scenario()` 함수 구현 (2025-12-21 23:27:35)
- [x] `calculate_scenario()` 함수 구현 (2025-12-21 23:27:40)
- [x] `compare_scenarios()` 함수 구현 (2025-12-21 23:27:48)
- [x] 기본 시나리오 목록 정의 (문서화)
- [x] 타입 힌트 추가
- [x] docstring 작성

---

## 테스트 계획

### 테스트 항목

1. **시나리오 파싱 테스트**
   - 단일 변경사항 파싱
   - 복합 변경사항 파싱
   - 잘못된 형식 처리

2. **시나리오 계산 테스트**
   - 지출 감소 시나리오
   - 연봉 증가 시나리오
   - 복합 시나리오
   - 기본 시나리오와 비교

3. **여러 시나리오 비교 테스트**
   - 여러 시나리오 동시 계산
   - 최고/최저 시나리오 식별
   - 차이 계산

---

## 예상 결과

- 시나리오 비교 계산 로직이 완성됨
- 다양한 시나리오를 비교할 수 있음
- 사용자가 시나리오를 입력하여 비교 가능
- 다음 작업(데이터 포맷팅 모듈)을 시작할 수 있는 상태

---

## 다음 작업

작업 1.8: 데이터 포맷팅 모듈 구현


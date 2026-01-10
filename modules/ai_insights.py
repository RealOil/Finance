"""
AI 기반 인사이트 생성 모듈

OpenAI API를 사용하여 재정 상태에 대한 맞춤형 인사이트를 생성합니다.
환경 변수로 활성화/비활성화 가능합니다.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


def is_ai_enabled() -> bool:
    """
    AI 기능 활성화 여부 확인

    Returns:
        bool: OPENAI_API_KEY가 설정되어 있으면 True
    """
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key is not None and api_key.strip() != ""


def generate_ai_insight(
    inputs: Dict[str, Any],
    calculation_results: Dict[str, Any],
    context: str = "재정 상태 분석",
) -> Optional[str]:
    """
    OpenAI API를 사용하여 재정 상태 기반 인사이트 생성

    Args:
        inputs: 입력 데이터 딕셔너리
        calculation_results: 계산 결과 딕셔너리
        context: 인사이트 맥락 설명

    Returns:
        Optional[str]: 생성된 인사이트 텍스트 (API 호출 실패 시 None)
    """
    if not is_ai_enabled():
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # 입력 데이터 요약
        summary = _create_summary(inputs, calculation_results)

        # 프롬프트 구성
        prompt = f"""
다음은 사용자의 재정 상태 분석 결과입니다.

{summary}

위 데이터를 바탕으로 **노후생활(연금) 계획에 중점을 둔** 마크다운 형식으로 다음과 같이 작성해주세요:

## 📊 재정 상태 분석

현재 재정 상태를 노후생활 준비 관점에서 분석해주세요. 은퇴 시점까지의 자산 형성 가능성, 현재 저축 능력, 부채 상황이 노후에 미치는 영향을 중심으로 설명해주세요.

## 💡 실행 가능한 조언

**노후생활을 위한 구체적이고 실행 가능한 조언**을 우선순위별로 제공해주세요. 대출 관리보다는 **연금 목표 달성, 저축 및 투자 전략, 자산 형성 계획**에 중점을 두어주세요.

각 조언은 다음과 같은 형식으로 작성해주세요:

### 🔴 높은 우선순위
- [노후생활을 위한 구체적인 행동 계획 1] (예: "현재 월 100만원 저축을 150만원으로 늘려 10년간 연 5% 수익률로 투자하면 은퇴 시점에 약 X억원 추가 확보 가능")
- [노후생활을 위한 구체적인 행동 계획 2]

### 🟡 중간 우선순위
- [노후생활을 위한 구체적인 행동 계획 3]

### 🟢 낮은 우선순위
- [노후생활을 위한 구체적인 행동 계획 4]

**포함할 내용:**
- 은퇴 목표 자산 달성을 위한 월 저축액 제안
- 다양한 수익률 시나리오에서의 자산 형성 전망
- 대출 만료 후 저축 가능액 증가를 활용한 노후 자산 형성 계획
- 연금(퇴직연금, IRP, 개인연금 등) 활용 방안
- 인플레이션을 고려한 실질 자산 가치 계산

**⚠️ 중요한 재테크 원칙 (반드시 포함):**
- **분산 투자 전략**: "계란을 한 바구니에 넣지 말라"는 원칙에 따라 예금/적금, 주식, 채권, 부동산 등 다양한 자산군에 분산 투자할 것을 강조
- **자산 배분 (Asset Allocation)**: 나이와 은퇴까지 남은 기간을 고려한 적절한 자산 배분 비율 제안
- **리스크 관리**: 고수익을 추구하기 전에 리스크를 분산하고, 안정적 자산과 성장 자산의 균형 유지
- **단일 자산군 집중의 위험성**: 특정 자산군(예: 주식만, 부동산만)에 집중하지 말고 포트폴리오를 다양화할 것을 조언

각 조언은 구체적인 숫자, 기간, 수익률을 포함하여 실행 가능하도록 작성해주세요.

## 📈 장기 노후생활 계획

현재 나이부터 은퇴 시점까지의 장기 노후생활 준비 계획을 수립해주세요. 다음을 포함해주세요:

1. **현재 저축액으로 은퇴 시점 예상 자산**: 현재 저축 능력을 유지할 경우 예상 자산
2. **저축 증가 시나리오**: 저축액을 늘릴 경우의 자산 형성 전망
3. **투자 수익률별 시나리오**: 다양한 수익률(3%, 5%, 7%)에서의 자산 형성 전망
4. **대출 만료 후 시나리오**: 대출이 끝난 후 저축 가능액 증가를 활용한 자산 형성
5. **은퇴 후 생활비 대비 충족도**: 목표 은퇴 생활비 대비 충족 가능한 정도

## 💼 자산 배분 및 분산 투자 전략

**분산 투자의 중요성**을 강조하고, 다음과 같은 내용을 포함해주세요:

1. **현재 자산 배분 분석** (있는 경우): 현재 투자 포트폴리오의 자산 배분 비율 분석
2. **권장 자산 배분**: 나이와 은퇴까지 남은 기간을 고려한 적절한 자산 배분 비율 제안
   - 예: 안정 자산(예금/적금) 30%, 성장 자산(주식/ETF) 50%, 대체 투자(부동산/채권) 20%
3. **분산 투자의 이점**: 리스크 분산, 수익률 안정화, 시장 변동성에 대한 대응력 향상
4. **단일 자산군 집중의 위험**: 특정 자산군에만 투자할 경우의 리스크 설명
5. **구체적인 포트폴리오 구성 예시**: 예금/적금, 주식, 채권, 부동산, 연금 등 각 자산군의 역할과 비중

모든 시나리오는 구체적인 숫자와 기간을 포함하여 제시해주세요.

한국어로 자연스럽고 전문적인 톤으로 작성해주세요. 모든 숫자는 만원 단위로 표시해주세요. **대출 상환보다는 노후생활 자산 형성에 중점**을 두고, **분산 투자와 자산 배분의 중요성을 반드시 강조**해주세요.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 노후생활 계획 전문 재정 컨설턴트입니다. 사용자의 재정 상태를 분석하여 노후생활(연금) 준비에 중점을 둔 구체적이고 실행 가능한 조언을 제공합니다. 마크다운 형식으로 구조화된 응답을 제공합니다. 대출 관리보다는 은퇴 목표 자산 달성, 저축 및 투자 전략, 장기 자산 형성 계획에 초점을 맞춥니다. 특히 분산 투자(예금/적금, 주식, 채권, 부동산 등)와 자산 배분의 중요성을 반드시 강조하며, 단일 자산군에 집중하는 위험성을 설명합니다.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=2500,
        )

        insight = response.choices[0].message.content.strip()
        return insight

    except ImportError:
        # openai 패키지가 설치되지 않은 경우
        return None
    except Exception as e:
        # API 호출 실패 (API 키 오류, 네트워크 오류 등)
        print(f"AI 인사이트 생성 실패: {e}")
        return None


def _create_summary(inputs: Dict[str, Any], calculation_results: Dict[str, Any]) -> str:
    """
    입력 데이터와 계산 결과를 요약하여 텍스트로 변환

    Args:
        inputs: 입력 데이터 딕셔너리
        calculation_results: 계산 결과 딕셔너리

    Returns:
        str: 요약 텍스트
    """
    summary_lines = []

    # 기본 정보 (노후 계획에 필요한 핵심 정보만)
    summary_lines.append("=== 기본 정보 ===")
    summary_lines.append(f"현재 나이: {inputs.get('current_age', 0)}세")
    summary_lines.append(f"은퇴 예정 나이: {inputs.get('retirement_age', 0)}세")
    summary_lines.append(
        f"은퇴까지 남은 기간: {inputs.get('retirement_age', 0) - inputs.get('current_age', 0)}년"
    )

    # 소득 정보
    annual_income = inputs.get("salary", 0) + inputs.get("bonus", 0)
    summary_lines.append(f"연봉: {inputs.get('salary', 0):,}만원")
    if inputs.get("bonus", 0) > 0:
        summary_lines.append(f"상여금: {inputs.get('bonus', 0):,}만원")
    summary_lines.append(f"연간 총 소득: {annual_income:,}만원")

    # 자산 및 부채 (요약)
    total_assets = inputs.get("total_assets", 0)
    total_debt = inputs.get("total_debt", 0)
    summary_lines.append(f"\n=== 자산 및 부채 ===")
    summary_lines.append(f"총 자산: {total_assets:,}만원")
    summary_lines.append(f"총 부채: {total_debt:,}만원")
    if total_assets > 0:
        debt_ratio = (total_debt / total_assets) * 100
        summary_lines.append(f"자산 대비 부채 비율: {debt_ratio:.1f}%")

    # 현재 보유 자산 배분 (자산 배분 분석에 필수)
    asset_items = inputs.get("asset_items", [])
    if asset_items and total_assets > 0:
        summary_lines.append(f"\n=== 현재 보유 자산 배분 ===")

        # 자산 유형별 집계
        assets_by_type = {}
        portfolio_weighted_return = 0.0
        total_weighted_return = 0.0

        for item in asset_items:
            asset_type = item.get("type", "기타")
            value = (
                item.get("value", 0)
                or item.get("principal", 0)
                or item.get("amount", 0)
            )
            return_rate = item.get("return_rate", 0.0)

            # 만원 단위로 변환 (원 단위일 수 있음)
            if value >= 10000:
                value = value / 10000.0

            if asset_type not in assets_by_type:
                assets_by_type[asset_type] = {
                    "value": 0,
                    "return_rate": 0.0,
                    "count": 0,
                }

            assets_by_type[asset_type]["value"] += value
            assets_by_type[asset_type]["count"] += 1
            # 가중 평균 수익률 계산을 위한 준비
            total_weighted_return += value * return_rate

        # 자산 유형별 비중 및 수익률
        for asset_type, data in assets_by_type.items():
            value = data["value"]
            percentage = (value / total_assets * 100) if total_assets > 0 else 0
            avg_return = (
                (total_weighted_return / total_assets) if total_assets > 0 else 0.0
            )
            summary_lines.append(f"{asset_type}: {value:,.0f}만원 ({percentage:.1f}%)")

        # 포트폴리오 전체 수익률
        if total_assets > 0:
            portfolio_return = total_weighted_return / total_assets
            summary_lines.append(
                f"포트폴리오 가중 평균 수익률: {portfolio_return:.2f}%"
            )

    # 지출 및 저축 (노후 계획의 핵심)
    if "monthly_fixed_expense" in inputs and "monthly_variable_expense" in inputs:
        monthly_expense = inputs.get("monthly_fixed_expense", 0) + inputs.get(
            "monthly_variable_expense", 0
        )
    else:
        monthly_expense = inputs.get("monthly_expense", 0)

    annual_expense = monthly_expense * 12
    monthly_savings = calculation_results.get("monthly_savings", 0)

    summary_lines.append(f"\n=== 지출 및 저축 ===")
    summary_lines.append(f"연간 지출: {annual_expense:,}만원")
    summary_lines.append(f"월 저축 가능액: {monthly_savings:,.0f}만원")
    summary_lines.append(f"연간 저축 가능액: {monthly_savings * 12:,.0f}만원")

    if annual_income > 0:
        expense_ratio = (annual_expense / annual_income) * 100
        savings_ratio = ((monthly_savings * 12) / annual_income) * 100
        summary_lines.append(f"소득 대비 지출 비율: {expense_ratio:.1f}%")
        summary_lines.append(f"소득 대비 저축 비율: {savings_ratio:.1f}%")

    # 대출 정보 (노후 계획에 필요한 요약 정보만)
    debt_items = inputs.get("debt_items", [])
    if debt_items:
        active_debt_items = [
            item
            for item in debt_items
            if item.get("remaining_months", 0) > 0
            or item.get("remaining_months") is None
        ]
        if active_debt_items:
            total_monthly_debt_payment = sum(
                item.get("monthly_payment", 0) for item in active_debt_items
            )

            summary_lines.append(f"\n=== 대출 요약 (노후 계획 영향) ===")
            summary_lines.append(
                f"월 대출 상환액: {total_monthly_debt_payment:,.0f}만원"
            )

            # 대출 만료 시점 및 만료 후 저축 가능액 (노후 계획에 중요)
            max_remaining_months = max(
                item.get("remaining_months", 0) or 0 for item in active_debt_items
            )
            if max_remaining_months > 0:
                years = max_remaining_months // 12
                months = max_remaining_months % 12
                summary_lines.append(f"가장 긴 대출 만료까지: {years}년 {months}개월")

                savings_after_debt_paid = monthly_savings + total_monthly_debt_payment
                summary_lines.append(
                    f"대출 만료 후 월 저축 가능액: {savings_after_debt_paid:,.0f}만원 "
                    f"(현재 대비 월 {total_monthly_debt_payment:,.0f}만원 증가)"
                )

                # 전세자금 대출이 있는 경우 간단히 표시
                jeonse_loans = [
                    item for item in active_debt_items if item.get("is_jeonse", False)
                ]
                if jeonse_loans:
                    jeonse_total = sum(
                        item.get("principal", 0) for item in jeonse_loans
                    )
                    summary_lines.append(
                        f"전세자금 대출: {jeonse_total:,.0f}만원 (만기 시 보증금 반환으로 원금 상환, 자산 감소 없음)"
                    )

    # 현재 투자 포트폴리오 정보 (있다면)
    monthly_investment_items = inputs.get("monthly_investment_items", [])
    if monthly_investment_items:
        summary_lines.append(f"\n=== 현재 투자 포트폴리오 ===")
        total_monthly_investment = sum(
            item.get("monthly_amount", 0) / 10000.0 for item in monthly_investment_items
        )  # 만원 단위로 변환

        summary_lines.append(f"월 투자액 합계: {total_monthly_investment:,.0f}만원")

        # 자산 유형별 집계
        investment_by_type = {}
        for item in monthly_investment_items:
            asset_type = item.get("type", "기타")
            amount = item.get("monthly_amount", 0) / 10000.0  # 만원 단위
            if asset_type not in investment_by_type:
                investment_by_type[asset_type] = 0
            investment_by_type[asset_type] += amount

        if investment_by_type:
            summary_lines.append("자산 유형별 투자액:")
            for asset_type, amount in investment_by_type.items():
                percentage = (
                    (amount / total_monthly_investment * 100)
                    if total_monthly_investment > 0
                    else 0
                )
                summary_lines.append(
                    f"  - {asset_type}: {amount:,.0f}만원 ({percentage:.1f}%)"
                )

    # 계산 결과 (노후 계획에 필요한 핵심 정보만)
    if "future_assets" in calculation_results:
        future_result = calculation_results["future_assets"]
        summary_lines.append(f"\n=== 미래 자산 추정 (노후 계획) ===")
        summary_lines.append(
            f"은퇴 시점 예상 자산: {future_result.get('future_assets', 0):,}만원"
        )
        summary_lines.append(
            f"현재 자산 대비 증가액: {future_result.get('future_assets', 0) - total_assets:,}만원"
        )

        # 은퇴 후 생활비 정보 (있다면)
        retirement_monthly_expense = inputs.get("retirement_monthly_expense", 0)
        if retirement_monthly_expense > 0:
            summary_lines.append(
                f"은퇴 후 예상 월 생활비: {retirement_monthly_expense:,.0f}만원"
            )
            summary_lines.append(
                f"은퇴 후 예상 연 생활비: {retirement_monthly_expense * 12:,.0f}만원"
            )

            # 4% 현금화율 기준 자산 필요액 계산
            target_assets_for_retirement = (retirement_monthly_expense * 12) / 0.04
            summary_lines.append(
                f"은퇴 후 생활비 충족 목표 자산 (4% 현금화율 기준): {target_assets_for_retirement:,.0f}만원"
            )

    # 은퇴 목표 계산 결과 (있다면)
    if "retirement_goal" in calculation_results:
        goal_result = calculation_results["retirement_goal"]
        summary_lines.append(f"\n=== 은퇴 목표 계산 결과 ===")
        summary_lines.append(f"목표 자산: {goal_result.get('target_assets', 0):,}만원")
        summary_lines.append(
            f"월 저축액 (시나리오): {goal_result.get('monthly_contribution', 0):,.0f}만원"
        )
        summary_lines.append(
            f"예상 수익률: {goal_result.get('annual_return_rate', 0):.1f}%"
        )

    return "\n".join(summary_lines)

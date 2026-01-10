"""
데이터 포맷팅 모듈

숫자 포맷팅과 인사이트 텍스트 생성을 담당합니다.
"""

from typing import Dict, Any


def format_currency(value: float, unit: str = "만원") -> str:
    """
    금액 포맷팅

    Args:
        value: 금액 (만원 단위)
        unit: 단위 (기본값: "만원")

    Returns:
        str: 포맷팅된 금액 문자열
    """
    if value is None:
        return f"0{unit}"

    # 반올림
    rounded_value = round(value)

    # 천 단위 구분 기호 추가
    formatted = f"{rounded_value:,}"

    return f"{formatted}{unit}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    퍼센트 포맷팅

    Args:
        value: 퍼센트 값
        decimals: 소수점 자릿수 (기본값: 1)

    Returns:
        str: 포맷팅된 퍼센트 문자열
    """
    if value is None:
        return "0.0%"

    formatted = f"{value:.{decimals}f}"
    return f"{formatted}%"


def format_number(value: float, decimals: int = 0) -> str:
    """
    일반 숫자 포맷팅

    Args:
        value: 숫자 값
        decimals: 소수점 자릿수 (기본값: 0)

    Returns:
        str: 포맷팅된 숫자 문자열
    """
    if value is None:
        return "0"

    if decimals == 0:
        rounded_value = round(value)
        return f"{rounded_value:,}"
    else:
        formatted = f"{value:,.{decimals}f}"
        return formatted


def generate_financial_health_insight(grade_result: Dict[str, Any]) -> str:
    """
    재정 건전성 등급 인사이트 생성

    Args:
        grade_result: 재정 건전성 등급 결과

    Returns:
        str: 인사이트 텍스트
    """
    grade = grade_result.get("grade", "D")
    expense_ratio = grade_result.get("expense_ratio", 0)
    monthly_savings = grade_result.get("monthly_savings", 0)

    insights = {
        "A+": f"매우 건강한 재정 상태입니다! 소득 대비 지출이 {format_percentage(expense_ratio)}로 낮고, "
        f"월 저축 가능액이 {format_currency(monthly_savings)}입니다. 현재 패턴을 유지하시면 "
        f"안정적인 미래를 기대할 수 있습니다.",
        "A": f"건강한 재정 상태입니다. 소득 대비 지출이 {format_percentage(expense_ratio)}이고, "
        f"월 저축 가능액이 {format_currency(monthly_savings)}입니다. 현재의 저축 습관을 유지하세요.",
        "B": f"보통 수준의 재정 상태입니다. 소득 대비 지출이 {format_percentage(expense_ratio)}입니다. "
        f"지출을 조금 줄이면 더 많은 저축이 가능합니다.",
        "C": f"재정 상태 개선이 필요합니다. 소득 대비 지출이 {format_percentage(expense_ratio)}로 높습니다. "
        f"지출을 줄이고 저축을 늘리는 것을 권장합니다.",
        "D": f"재정 상태가 위험합니다. 소득 대비 지출이 {format_percentage(expense_ratio)}입니다. "
        f"즉시 지출을 줄이고 저축 계획을 수립하세요.",
    }

    return insights.get(grade, insights["D"])


def generate_risk_insight(risk_result: Dict[str, Any]) -> str:
    """
    위험도 점수 인사이트 생성

    Args:
        risk_result: 위험도 점수 결과

    Returns:
        str: 인사이트 텍스트
    """
    total_score = risk_result.get("total_score", 0)
    risk_level = risk_result.get("risk_level", "medium")
    recommendations = risk_result.get("recommendations", [])

    risk_messages = {
        "low": f"위험도 점수가 {total_score}점으로 낮습니다. 현재 재정 상태가 안정적입니다.",
        "medium": f"위험도 점수가 {total_score}점입니다. 일부 개선이 필요합니다.",
        "high": f"위험도 점수가 {total_score}점으로 높습니다. 재정 상태 개선이 시급합니다.",
        "critical": f"위험도 점수가 {total_score}점으로 매우 높습니다. 즉시 조치가 필요합니다.",
    }

    base_message = risk_messages.get(risk_level, risk_messages["medium"])

    if recommendations:
        rec_text = " ".join([f"• {rec}" for rec in recommendations])
        return f"{base_message}\n\n권장사항:\n{rec_text}"

    return base_message


def generate_future_assets_insight(future_assets_result: Dict[str, Any]) -> str:
    """
    미래 자산 추정 인사이트 생성

    Args:
        future_assets_result: 미래 자산 추정 결과

    Returns:
        str: 인사이트 텍스트
    """
    current_assets = future_assets_result.get("current_assets", 0)
    future_assets = future_assets_result.get("future_assets", 0)
    total_savings = future_assets_result.get("total_savings", 0)
    years = future_assets_result.get("years", 10)

    if future_assets > current_assets:
        growth = (
            ((future_assets - current_assets) / current_assets * 100)
            if current_assets > 0
            else 0
        )
        return (
            f"{years}년 후 예상 자산은 {format_currency(future_assets)}입니다. "
            f"현재 자산 {format_currency(current_assets)} 대비 {format_percentage(growth)} 증가하며, "
            f"총 {format_currency(total_savings)}를 저축할 수 있습니다."
        )
    else:
        return (
            f"{years}년 후 예상 자산은 {format_currency(future_assets)}입니다. "
            f"현재 자산보다 감소할 것으로 예상됩니다. 지출을 줄이고 저축을 늘리는 것이 필요합니다."
        )


def generate_retirement_insight(retirement_result: Dict[str, Any]) -> str:
    """
    은퇴 시나리오 인사이트 생성

    Args:
        retirement_result: 은퇴 시나리오 결과

    Returns:
        str: 인사이트 텍스트
    """
    years_to_retirement = retirement_result.get("years_to_retirement", 0)
    expected_assets = retirement_result.get("expected_assets_at_retirement", 0)
    survival_years = retirement_result.get("survival_years", 0)
    life_expectancy = retirement_result.get("life_expectancy_after_retirement", 20)
    is_sustainable = retirement_result.get("is_sustainable", False)

    if is_sustainable:
        return (
            f"은퇴까지 {years_to_retirement}년 남았습니다. "
            f"은퇴 시점 예상 자산은 {format_currency(expected_assets)}이며, "
            f"은퇴 후 약 {survival_years:.1f}년간 생활비를 유지할 수 있습니다. "
            f"기대 수명({life_expectancy}년)을 고려할 때 충분합니다."
        )
    else:
        return (
            f"은퇴까지 {years_to_retirement}년 남았습니다. "
            f"은퇴 시점 예상 자산은 {format_currency(expected_assets)}이며, "
            f"은퇴 후 약 {survival_years:.1f}년간 생활비를 유지할 수 있습니다. "
            f"기대 수명({life_expectancy}년) 대비 부족하므로 추가 저축이 필요합니다."
        )


def get_status_message(status: str, category: str = "general") -> str:
    """
    상태별 메시지 반환

    Args:
        status: 상태 코드 (safe, warning, danger, sustainable, low, medium, high, critical)
        category: 카테고리 (general, income, retirement, risk)

    Returns:
        str: 상태 메시지
    """
    messages = {
        "safe": "안전한 상태입니다.",
        "warning": "주의가 필요합니다.",
        "danger": "위험한 상태입니다. 즉시 조치가 필요합니다.",
        "sustainable": "지속 가능한 상태입니다.",
        "low": "위험도가 낮습니다.",
        "medium": "위험도가 보통입니다.",
        "high": "위험도가 높습니다.",
        "critical": "위험도가 매우 높습니다.",
    }

    return messages.get(status, "상태를 확인할 수 없습니다.")


def generate_comprehensive_insights(
    inputs: Dict[str, Any],
    calculation_results: Dict[str, Any],
    use_ai: bool = False,
) -> Dict[str, Any]:
    """
    종합 인사이트 생성 (AI 전용)

    참고: 이 함수는 이전 버전 호환성을 위해 유지되지만,
    이제는 AI 인사이트만 사용합니다.

    Args:
        inputs: 입력 데이터 딕셔너리
        calculation_results: 계산 결과 딕셔너리
        use_ai: AI 사용 여부 (사용되지 않음, AI가 활성화되어 있으면 항상 실행)

    Returns:
        Dict[str, Any]: 종합 인사이트
            - ai_insight: AI 생성 인사이트 (있는 경우)
    """
    from modules.ai_insights import generate_ai_insight, is_ai_enabled

    result = {
        "ai_insight": None,
    }

    # AI 인사이트 생성 (AI가 활성화된 경우만)
    if is_ai_enabled():
        ai_insight = generate_ai_insight(inputs, calculation_results)
        if ai_insight:
            result["ai_insight"] = ai_insight

    return result

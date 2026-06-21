import structlog
from datetime import datetime

from langchain_core.tools import tool

from src.integrations.finances import client as finances_client
from src.integrations.finances.exceptions import FinanceIntegrationError

logger = structlog.get_logger(__name__)

OBLIGATION_CATEGORIES = {"mortgage", "rent", "loan", "car loan", "personal loan", "credit"}


def _compute_emi(loan_amount: float, monthly_rate: float, n: int) -> float:
    if monthly_rate == 0:
        return loan_amount / n
    return loan_amount * (monthly_rate * (1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)


def _count_major_obligations() -> int:
    date = datetime.now().strftime("%Y-%m")
    report = finances_client.get_report_by_month(date)
    return sum(
        1 for cat in report.categories
        if any(keyword in cat.lower() for keyword in OBLIGATION_CATEGORIES)
    )


@tool(description=(
    "Determine if the user can afford a car based on their financial situation. "
    "Use when the user asks about their ability to purchase a car. "
    "car_price is the total purchase price in EUR. "
    "interest_rate is the annual rate in percent, defaults to 5."
))
def can_i_afford_a_car(car_price: float, interest_rate: float = 5.0) -> str:
    logger.info("Invoking can_i_afford_a_car", car_price=car_price, interest_rate=interest_rate)

    if car_price <= 0:
        return "Car price must be a positive number."

    try:
        m = finances_client.get_health_metrics()
    except FinanceIntegrationError as e:
        return f"Could not fetch financial data: {e.message}"

    monthly_income = m.averageMonthlyIncome
    liquid_savings = m.totalAccountBalance

    # Rule 1: 20% down payment
    down_payment = car_price * 0.20
    can_afford_down = liquid_savings >= down_payment

    # Rule 2: EMI ≤ 10% of monthly income over 4 years
    loan_amount = car_price - down_payment
    emi = _compute_emi(loan_amount, interest_rate / 100 / 12, 48)
    max_emi = monthly_income * 0.10
    can_afford_emi = emi <= max_emi

    # Rule 3: No more than 2 existing major obligations
    try:
        obligations = _count_major_obligations()
        can_afford_obligations = obligations <= 2
        obligation_line = (
            f"Existing obligations: {obligations} — "
            f"{'OK' if can_afford_obligations else 'FAIL'} (max 2)\n"
        )
    except FinanceIntegrationError:
        can_afford_obligations = True  # don't block on missing data
        obligation_line = "Existing obligations: could not determine\n"

    affordable = can_afford_down and can_afford_emi and can_afford_obligations
    verdict = "✅ Affordable" if affordable else "❌ Not affordable"

    return (
        f"Car price: €{car_price:,.2f}\n"
        f"Down payment (20%): €{down_payment:,.2f} — "
        f"{'OK' if can_afford_down else 'FAIL'} (you have €{liquid_savings:,.2f})\n"
        f"Monthly EMI (4yr @ {interest_rate}%): €{emi:,.2f} — "
        f"{'OK' if can_afford_emi else 'FAIL'} (max €{max_emi:,.2f} = 10% of income)\n"
        f"{obligation_line}"
        f"\n{verdict}"
    )


@tool(description=(
    "Determine if the user can afford a phone based on their financial situation. "
    "Use when the user asks about their ability to purchase a phone. "
    "price is the total purchase price in EUR. "
    "interest_rate is the annual rate in percent, defaults to 0 for typical 0% installment plans."
))
def can_i_afford_a_phone(price: float, interest_rate: float = 0.0) -> str:
    logger.info("Invoking can_i_afford_a_phone", price=price, interest_rate=interest_rate)

    if price <= 0:
        return "Phone price must be a positive number."

    try:
        m = finances_client.get_health_metrics()
    except FinanceIntegrationError as e:
        return f"Could not fetch financial data: {e.message}"

    monthly_income = m.averageMonthlyIncome

    # Rule 1: price ≤ 2x monthly income
    can_afford_total = price <= (2 * monthly_income)

    # Rule 2: EMI target ≤ 5%, hard max 10% of monthly income over 6 months
    emi = _compute_emi(price, interest_rate / 100 / 12, 6)
    target_emi = monthly_income * 0.05
    max_emi = monthly_income * 0.10
    emi_ideal = emi <= target_emi
    emi_ok = emi <= max_emi

    if emi_ideal:
        emi_status = "OK"
    elif emi_ok:
        emi_status = "WARNING — between 5–10% of income"
    else:
        emi_status = "FAIL"

    affordable = can_afford_total and emi_ok
    verdict = "✅ Affordable" if affordable else "❌ Not affordable"
    if affordable and not emi_ideal:
        verdict += " (EMI above 5% target — consider carefully)"

    return (
        f"Phone price: €{price:,.2f}\n"
        f"Price vs 2x income: €{price:,.2f} vs €{2 * monthly_income:,.2f} — "
        f"{'OK' if can_afford_total else 'FAIL'}\n"
        f"Monthly EMI (6m @ {interest_rate}%): €{emi:,.2f} — "
        f"{emi_status} (target €{target_emi:,.2f}, max €{max_emi:,.2f})\n"
        f"\n{verdict}"
    )

from langchain_core.tools import tool
from src.integrations.finances import client as finances_client
from src.integrations.finances.exceptions import FinanceIntegrationError


@tool(description=(
    "Determine if the user can afford a car based on their financial situation. "
    "Use when the user asks about their ability to purchase a car."
))
def can_i_afford_a_car(car_price: float, interest_rate: int = 5):
    try:
        m = finances_client.get_health_metrics()
    except FinanceIntegrationError as e:
        return f"Could not fetch financial data: {e.message}"

    monthly_income = m.averageMonthlyIncome
    liquid_savings = m.totalAccountBalance

    # Rule 1: 20% down payment
    down_payment_needed = car_price * 0.20
    can_afford_down = liquid_savings >= down_payment_needed

    # Rule 2: EMI ≤ 10% of monthly income, 4-year loan
    loan_amount = car_price - down_payment_needed
    monthly_rate = interest_rate / 100 / 12
    n = 48
    emi = loan_amount * (monthly_rate * (1 + monthly_rate)**n) / ((1 + monthly_rate)**n - 1)
    max_emi = monthly_income * 0.10
    can_afford_emi = emi <= max_emi

    veredict = "❌ Not affordable"
    if can_afford_emi and can_afford_down:
        veredict = "✅ Affordable"

    return (
        f"Car price: €{car_price:,.2f}\n"
        f"Down payment needed (20%): €{down_payment_needed:,.2f} — "
        f"{'OK' if can_afford_down else 'FAIL'} (you have €{liquid_savings:,.2f})\n"
        f"Monthly EMI (4yr loan): €{emi:,.2f} — "
        f"{'OK' if can_afford_emi else 'FAIL'} (max €{max_emi:,.2f} = 10% of income)\n"
        f"\n{veredict}"
    )



@tool(description=(
    "Determine if the user can afford a phone based on their financial situation. "
    "Use when the user asks about their ability to purchase a phone."
))
def can_i_afford_a_phone(price: float, interest_rate: int = 5):
    """
    Rules:
    Cost must not exceed twice the monthly income
    Limit the loan to 6 months
    EMI should be 5%, 10% max of monthly income
    :return:
    """
    try:
        m = finances_client.get_health_metrics()
    except FinanceIntegrationError as e:
        return f"Could not fetch financial data: {e.message}"

    monthly_income = m.averageMonthlyIncome

    can_afford_total = price <= (2 * monthly_income)

    loan_amount = price
    monthly_rate = interest_rate / 100 / 12
    n = 6
    emi = loan_amount * (monthly_rate * (1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)
    max_emi = monthly_income * 0.10
    can_afford_emi = emi <= max_emi

    veredict = "❌ Not affordable"
    if can_afford_emi and can_afford_total:
        veredict = "✅ Affordable"

    return (
        f"Phone price: €{price:,.2f}\n"
        f"Price vs 2x income: €{price:,.2f} vs €{2 * monthly_income:,.2f} — {'OK' if can_afford_total else 'FAIL'}\n"
        f"Monthly EMI (6m loan): €{emi:,.2f} — "
        f"{'OK' if can_afford_emi else 'FAIL'} (max €{max_emi:,.2f} = 10% of income)\n"
        f"\n{veredict}"
    )
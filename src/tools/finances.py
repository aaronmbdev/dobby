from langchain_core.tools import tool

from src.integrations.finances import client
from src.integrations.finances.exceptions import FinanceIntegrationError
from src.integrations.finances.models import MonthlyReport


@tool(description=(
    "Get all bank and cash accounts with their current balance and last update date. "
    "Use when the user asks about their bank accounts, savings, cash position, or total liquid assets."
))
def get_accounts() -> str:
    try:
        accounts = client.get_accounts()
        if not accounts:
            return "No accounts found."
        lines = [
            f"- {a.name}: €{a.latestBalance:,.2f} (as of {a.latestBalanceDate})"
            for a in accounts
        ]
        total = sum(a.latestBalance for a in accounts)
        lines.append(f"\nTotal: €{total:,.2f}")
        return "\n".join(lines)
    except FinanceIntegrationError as e:
        return f"Could not fetch accounts: {e.message}"


@tool(description=(
    "Get the current stock portfolio: name, ticker, number of shares, latest price in EUR, "
    "and total value per position. "
    "Use when the user asks about their stocks, equity holdings, or individual stock positions."
))
def get_stocks() -> str:
    try:
        stocks = client.get_stocks()
        if not stocks:
            return "No stocks found."
        lines = []
        total = 0.0
        for s in stocks:
            value = s.latestPriceEur * s.latestShares
            total += value
            lines.append(
                f"- {s.name} ({s.ticker}): {s.latestShares} shares @ €{s.latestPriceEur:.2f}"
                f" = €{value:,.2f} (as of {s.latestDate})"
            )
        lines.append(f"\nTotal: €{total:,.2f}")
        return "\n".join(lines)
    except FinanceIntegrationError as e:
        return f"Could not fetch stocks: {e.message}"


@tool(description=(
    "Get the current investment fund portfolio: fund name, ISIN, number of shares, "
    "latest price in EUR, and total value per fund. "
    "Use when the user asks about their funds, index funds, ETFs, or fund portfolio."
))
def get_investment_funds() -> str:
    try:
        funds = client.get_investment_funds()
        if not funds:
            return "No investment funds found."
        lines = []
        total = 0.0
        for f in funds:
            value = f.latestPriceEur * f.latestShares
            total += value
            lines.append(
                f"- {f.name} ({f.isin}): {f.latestShares} shares @ €{f.latestPriceEur:.2f}"
                f" = €{value:,.2f} (as of {f.latestDate})"
            )
        lines.append(f"\nTotal: €{total:,.2f}")
        return "\n".join(lines)
    except FinanceIntegrationError as e:
        return f"Could not fetch investment funds: {e.message}"


@tool(description=(
    "Get the historical net worth over time, broken down into accounts, stocks, and funds. "
    "Use when the user asks about net worth evolution, total wealth growth, or asset trends over time. "
    "Returns all recorded monthly snapshots."
))
def get_net_worth_history() -> str:
    try:
        snapshots = client.get_net_worth_history()
        if not snapshots:
            return "No net worth history found."
        lines = [
            f"- {s.date}: €{s.total:,.2f}"
            f" (Accounts: €{s.accountsTotal:,.2f}"
            f", Stocks: €{s.stocksTotal:,.2f}"
            f", Funds: €{s.fundsTotal:,.2f})"
            for s in snapshots
        ]
        return "\n".join(lines)
    except FinanceIntegrationError as e:
        return f"Could not fetch net worth history: {e.message}"


@tool(description=(
    "Get key financial health indicators: savings rate, emergency fund coverage, "
    "housing ratio, investment ratio, debt-to-income ratio, and expense distribution. "
    "Use when the user asks about their financial health, whether they are saving enough, "
    "or wants a general overview of their financial situation."
))
def get_financial_health() -> str:
    try:
        m = client.get_health_metrics()
        return (
            f"Monthly Income:        €{m.averageMonthlyIncome:,.2f}\n"
            f"Monthly Burn:          €{m.totalMonthlyBurn:,.2f} (Essential: €{m.essentialMonthlyBurn:,.2f})\n"
            f"Total Account Balance: €{m.totalAccountBalance:,.2f}\n"
            f"Savings Rate:          {m.savingsRate}\n"
            f"Emergency Fund:        {m.emergencyFund}\n"
            f"Investment Ratio:      {m.investmentRatio}\n"
            f"Housing Ratio:         {m.housingRatio}\n"
            f"Debt to Income:        {m.debtToIncome}\n"
            f"Fixed vs Variable:     {m.fixedVsVariable}\n"
            f"Expense Growth Rate:   {m.expenseGrowthRate}"
        )
    except FinanceIntegrationError as e:
        return f"Could not fetch financial health metrics: {e.message}"


@tool(description=(
    "Get a detailed monthly financial report: all expenses listed by category, income, "
    "and an overview with total income, total expenses, and net balance. "
    "Use when the user asks about spending in a specific month, their expense breakdown, "
    "or how much they earned and spent. Date must be YYYY-MM-DD (any day within the target month)."
))
def get_monthly_report(date: str) -> str:
    try:
        report = client.get_report_by_month(date)
        return _format_monthly_report(report)
    except FinanceIntegrationError as e:
        return f"Could not fetch monthly report: {e.message}"


def _format_monthly_report(report: MonthlyReport) -> str:
    o = report.overview
    overview = (
        f"Overview:\n"
        f"  Income:   €{o.monthlyIncome:,.2f}\n"
        f"  Expenses: €{o.monthlyExpenses:,.2f}\n"
        f"  Balance:  €{o.balance:,.2f}"
    )

    categories = "Expenses by category:\n" + "\n".join(
        f"  {cat}: €{amount:,.2f}"
        for cat, amount in sorted(report.categories.items(), key=lambda x: -x[1])
    )

    transactions = "Transactions:\n" + "\n".join(
        f"  {e.date} | {e.category} | {e.description}: €{e.amount:,.2f}"
        for e in report.expenses
    )

    return f"{overview}\n\n{categories}\n\n{transactions}"

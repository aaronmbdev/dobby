import structlog
from datetime import datetime, UTC, timedelta

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.config.settings import settings
from src.goals.service import GoalService
from src.integrations.diet import client as diet_client
from src.integrations.finances import client as finances_client
from src.summaries.email import send_summary

logger = structlog.get_logger(__name__)

_llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model=settings.openai_model,
    temperature=0.3,
)

_WEEKLY_FINANCE_SYSTEM = SystemMessage(content="""
You are Dobby, a personal AI assistant generating a weekly financial report.
Analyse account balances, the investment portfolio (stocks and funds), and
current month expense progress. Map observations to the user's financial goals.
Write 6-10 points: portfolio performance, spending pace, goal progress,
and one actionable recommendation. Be specific with numbers.
Start every point with • and nothing else. One point per line. No headers. No other formatting.
""")

_WEEKLY_DIET_SYSTEM = SystemMessage(content="""
You are Dobby, a personal AI assistant generating a weekly diet quality report.
You have the full meal logs for the past 7 days: every food item, its weight in grams,
and macro breakdown per meal. Analyse:
- Macro adherence vs daily targets (days hit vs missed)
- Ingredient variety and recurring foods
- Missing food groups or nutritional gaps
- Overall diet quality
Provide 3-5 specific, actionable improvement recommendations.
Be honest but constructive.
Start every point with • and nothing else. One point per line. No headers. No other formatting.
""")

_WEEKLY_BODY_SYSTEM = SystemMessage(content="""
You are Dobby, a personal AI assistant generating a weekly body progress report.
Analyse weight, fat mass, muscle mass, and BMI trends across all available measurements.
Map progress to the user's health goals. Write 5-8 points: trends, notable changes,
goal progress, and one specific recommendation. Be precise with numbers.
Start every point with • and nothing else. One point per line. No headers. No other formatting.
""")

_MONTHLY_FINANCE_SYSTEM = SystemMessage(content="""
You are Dobby, a personal AI assistant generating a monthly financial review.
Analyse the full monthly expense report, income, financial health metrics, and net worth snapshot.
Map findings to the user's financial goals. Write 8-12 points covering:
income vs expenses, top spending categories, savings rate, net worth change, goal progress,
and 2 actionable recommendations for the coming month. Be specific with numbers.
Start every point with • and nothing else. One point per line. No headers. No other formatting.
""")


class SummaryService:

    def __init__(self) -> None:
        self._goals = GoalService()

    # ── Weekly reports ────────────────────────────────────────────────────────

    def send_weekly_finances(self) -> None:
        data = self._weekly_finance_data()
        content = _llm.invoke([_WEEKLY_FINANCE_SYSTEM, HumanMessage(content=data)]).content
        send_summary("Dobby — Weekly Finance Report", content)
        logger.info("weekly finance report sent")

    def send_weekly_diet(self) -> None:
        data = self._weekly_diet_data()
        content = _llm.invoke([_WEEKLY_DIET_SYSTEM, HumanMessage(content=data)]).content
        send_summary("Dobby — Weekly Diet Report", content)
        logger.info("weekly diet report sent")

    def send_weekly_body(self) -> None:
        data = self._weekly_body_data()
        content = _llm.invoke([_WEEKLY_BODY_SYSTEM, HumanMessage(content=data)]).content
        send_summary("Dobby — Weekly Body Progress", content)
        logger.info("weekly body report sent")

    # ── Monthly reports ───────────────────────────────────────────────────────

    def send_monthly_finances(self) -> None:
        data = self._monthly_finance_data()
        content = _llm.invoke([_MONTHLY_FINANCE_SYSTEM, HumanMessage(content=data)]).content
        send_summary("Dobby — Monthly Finance Report", content)
        logger.info("monthly finance report sent")

    # ── Data gathering ────────────────────────────────────────────────────────

    def _weekly_finance_data(self) -> str:
        parts = []

        try:
            accounts = finances_client.get_accounts()
            lines = [f"  {a.name}: €{a.latestBalance:,.2f}" for a in accounts]
            parts.append("Accounts:\n" + "\n".join(lines))
        except Exception:
            logger.warning("weekly finance: could not load accounts")

        try:
            stocks = finances_client.get_stocks()
            lines = [
                f"  {s.name} ({s.ticker}): {s.latestShares} shares @ €{s.latestPriceEur:.2f}"
                f" = €{s.latestPriceEur * s.latestShares:,.2f}"
                for s in stocks
            ]
            total = sum(s.latestPriceEur * s.latestShares for s in stocks)
            parts.append(f"Stocks (total €{total:,.2f}):\n" + "\n".join(lines))
        except Exception:
            logger.warning("weekly finance: could not load stocks")

        try:
            funds = finances_client.get_investment_funds()
            lines = [
                f"  {f.name}: {f.latestShares} shares @ €{f.latestPriceEur:.2f}"
                f" = €{f.latestPriceEur * f.latestShares:,.2f}"
                for f in funds
            ]
            total = sum(f.latestPriceEur * f.latestShares for f in funds)
            parts.append(f"Funds (total €{total:,.2f}):\n" + "\n".join(lines))
        except Exception:
            logger.warning("weekly finance: could not load funds")

        try:
            today = datetime.now(UTC).strftime("%Y-%m-%d")
            report = finances_client.get_report_by_month(today)
            o = report.overview
            parts.append(
                f"This month: income €{o.monthlyIncome:,.2f} | "
                f"expenses €{o.monthlyExpenses:,.2f} | "
                f"balance €{o.balance:,.2f}"
            )
            top = sorted(report.categories.items(), key=lambda x: -x[1])[:5]
            parts.append("Top expense categories:\n" + "\n".join(f"  {k}: €{v:,.2f}" for k, v in top))
        except Exception:
            logger.warning("weekly finance: could not load monthly report")

        parts.append(_format_goals(self._goals.list_active_by_domain("finances")))
        return "\n\n".join(parts)

    def _weekly_diet_data(self) -> str:
        parts = []
        today = datetime.now(UTC).date()

        for i in range(7):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            try:
                log = diet_client.get_daily_log(date)
                kcal = sum(m.total_macros.calories for m in log.meals)
                protein = sum(m.total_macros.protein for m in log.meals)
                carbs = sum(m.total_macros.carbs for m in log.meals)
                fat = sum(m.total_macros.fat for m in log.meals)

                meal_lines = []
                for meal in log.meals:
                    foods = ", ".join(f"{f.name} ({f.grams}g)" for f in meal.foods)
                    meal_lines.append(
                        f"  Meal: {foods} → "
                        f"{meal.total_macros.calories} kcal, "
                        f"{meal.total_macros.protein}g protein"
                    )

                parts.append(
                    f"{date}: {kcal}/{log.target.calories} kcal | "
                    f"protein {protein}/{log.target.protein}g | "
                    f"carbs {carbs}/{log.target.carbs}g | "
                    f"fat {fat}/{log.target.fat}g\n" +
                    "\n".join(meal_lines)
                )
            except Exception:
                logger.warning("weekly diet: could not fetch log", date=date)

        parts.append(_format_goals(self._goals.list_active_by_domain("diet")))
        return "\n\n".join(parts)

    def _weekly_body_data(self) -> str:
        parts = []

        try:
            metrics = sorted(diet_client.get_body_metrics(), key=lambda m: m.date)
            for m in metrics:
                parts.append(
                    f"{m.date}: {m.weightKg}kg | fat {m.fatKg}kg | "
                    f"muscle {m.muscleMassKg}kg | BMI {m.bmi} | "
                    f"visceral fat {m.visceralFat} | metabolic age {m.metabolicAge}"
                )
        except Exception:
            logger.warning("weekly body: could not load metrics")

        parts.append(_format_goals(self._goals.list_active_by_domain("health")))
        return "\n\n".join(parts)

    def _monthly_finance_data(self) -> str:
        parts = []

        try:
            first_of_month = datetime.now(UTC).replace(day=1)
            last_month = (first_of_month - timedelta(days=1)).strftime("%Y-%m-%d")
            report = finances_client.get_report_by_month(last_month)
            o = report.overview
            parts.append(
                f"Monthly overview: income €{o.monthlyIncome:,.2f} | "
                f"expenses €{o.monthlyExpenses:,.2f} | balance €{o.balance:,.2f}"
            )
            categories = sorted(report.categories.items(), key=lambda x: -x[1])
            parts.append("Expenses by category:\n" + "\n".join(f"  {k}: €{v:,.2f}" for k, v in categories))
            parts.append("Transactions:\n" + "\n".join(
                f"  {e.date} | {e.category} | {e.description}: €{e.amount:,.2f}"
                for e in report.expenses
            ))
        except Exception:
            logger.warning("monthly finance: could not load monthly report")

        try:
            m = finances_client.get_health_metrics()
            parts.append(
                f"Health metrics: savings rate {m.savingsRate} | "
                f"emergency fund {m.emergencyFund} | "
                f"investment ratio {m.investmentRatio} | "
                f"debt to income {m.debtToIncome}"
            )
        except Exception:
            logger.warning("monthly finance: could not load health metrics")

        try:
            snapshots = finances_client.get_net_worth_history()
            if snapshots:
                latest = max(snapshots, key=lambda s: s.date)
                parts.append(
                    f"Latest net worth ({latest.date}): €{latest.total:,.2f} "
                    f"(accounts €{latest.accountsTotal:,.2f}, "
                    f"stocks €{latest.stocksTotal:,.2f}, "
                    f"funds €{latest.fundsTotal:,.2f})"
                )
        except Exception:
            logger.warning("monthly finance: could not load net worth")

        parts.append(_format_goals(self._goals.list_active_by_domain("finances")))
        return "\n\n".join(parts)


def _format_goals(goals: list) -> str:
    if not goals:
        return "Financial goals: none set."
    lines = [f"  - [{g.domain}] {g.title}: {g.target}" + (f" (by {g.deadline})" if g.deadline else "") for g in goals]
    return "Goals:\n" + "\n".join(lines)

import structlog
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.config.settings import settings
from src.goals.service import GoalService
from src.integrations.diet import client as diet_client
from src.integrations.finances import client as finances_client
from src.summaries.repository import SummaryRepository

logger = structlog.get_logger(__name__)

_llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model=settings.openai_model,
    temperature=0.3,
)

_SYSTEM = SystemMessage(content="""
You are Dobby, a personal AI assistant writing a scheduled summary for your user.
Write a concise, friendly summary in 5-8 bullet points covering what is noteworthy,
unexpected, or actionable. Use plain language. No headers. No markdown formatting.
""")


class SummaryService:

    def __init__(self) -> None:
        self.repository = SummaryRepository()
        self._goal_service = GoalService()

    def generate_and_save(self, summary_type: str) -> None:
        data = self._gather_data(summary_type)
        content = self._generate(summary_type, data)
        self.repository.save(summary_type, content)
        logger.info("summary saved", type=summary_type)

    def _generate(self, summary_type: str, data: str) -> str:
        period = "weekly" if summary_type == "weekly" else "monthly"
        result = _llm.invoke([
            _SYSTEM,
            HumanMessage(content=f"Generate a {period} summary based on this data:\n\n{data}"),
        ])
        return result.content

    def _gather_data(self, summary_type: str) -> str:
        parts = [f"Summary type: {summary_type}"]

        try:
            m = finances_client.get_health_metrics()
            parts.append(
                f"Finances: balance €{m.totalAccountBalance:,.0f} | "
                f"avg monthly income €{m.averageMonthlyIncome:,.0f} | "
                f"avg monthly burn €{m.totalMonthlyBurn:,.0f} | "
                f"savings rate: {m.savingsRate}"
            )
        except Exception:
            logger.warning("summary: could not load financial data")

        try:
            metrics = sorted(diet_client.get_body_metrics(), key=lambda m: m.date)
            if len(metrics) >= 2:
                latest, previous = metrics[-1], metrics[-2]
                parts.append(
                    f"Body (latest {latest.date}): {latest.weightKg}kg, "
                    f"fat {latest.fatKg}kg, muscle {latest.muscleMassKg}kg. "
                    f"Previous ({previous.date}): {previous.weightKg}kg."
                )
            elif metrics:
                m = metrics[-1]
                parts.append(f"Body ({m.date}): {m.weightKg}kg, fat {m.fatKg}kg, muscle {m.muscleMassKg}kg.")
        except Exception:
            logger.warning("summary: could not load body metrics")

        try:
            log = diet_client.get_daily_log()
            kcal = sum(meal.total_macros.calories for meal in log.meals)
            protein = sum(meal.total_macros.protein for meal in log.meals)
            parts.append(
                f"Diet today ({log.date}): {kcal}/{log.target.calories} kcal, "
                f"{protein}/{log.target.protein}g protein."
            )
        except Exception:
            logger.warning("summary: could not load diet data")

        try:
            goals = self._goal_service.list_active()
            if goals:
                lines = [f"  - [{g.domain}] {g.title}: {g.target}" for g in goals]
                parts.append("Active goals:\n" + "\n".join(lines))
        except Exception:
            logger.warning("summary: could not load goals")

        return "\n".join(parts)

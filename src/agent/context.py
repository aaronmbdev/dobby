import structlog
from datetime import datetime, UTC

from langchain_core.messages import SystemMessage

from src.integrations.diet import client as diet_client
from src.integrations.diet.models import DayLog
from src.integrations.finances import client as finances_client

logger = structlog.get_logger(__name__)


def build_context() -> SystemMessage:
    parts = [f"Today is {datetime.now(UTC).strftime('%A, %d %B %Y')}."]

    _add_financial_context(parts)
    _add_diet_context(parts)
    _add_body_context(parts)

    return SystemMessage(content="\n".join(parts))


def _add_financial_context(parts: list[str]) -> None:
    try:
        m = finances_client.get_health_metrics()
        parts.append(
            f"Finances: €{m.totalAccountBalance:,.0f} total balance | "
            f"avg monthly income €{m.averageMonthlyIncome:,.0f}, burn €{m.totalMonthlyBurn:,.0f}"
        )
    except Exception:
        logger.warning("context: could not load financial snapshot")


def _add_diet_context(parts: list[str]) -> None:
    try:
        log = diet_client.get_daily_log()
        consumed = _sum_macros(log)
        t = log.target
        parts.append(
            f"Diet today ({log.date}): "
            f"{consumed.calories}/{t.calories} kcal | "
            f"protein {consumed.protein}/{t.protein}g | "
            f"carbs {consumed.carbs}/{t.carbs}g | "
            f"fat {consumed.fat}/{t.fat}g"
        )
    except Exception:
        logger.warning("context: could not load today's diet log")


def _add_body_context(parts: list[str]) -> None:
    try:
        metrics = diet_client.get_body_metrics()
        if metrics:
            latest = max(metrics, key=lambda m: m.date)
            parts.append(
                f"Last body check-in ({latest.date}): "
                f"{latest.weightKg}kg | "
                f"fat {latest.fatKg}kg | "
                f"muscle {latest.muscleMassKg}kg | "
                f"BMI {latest.bmi}"
            )
    except Exception:
        logger.warning("context: could not load body metrics")


def _sum_macros(log: DayLog):
    calories = sum(meal.total_macros.calories for meal in log.meals)
    protein = sum(meal.total_macros.protein for meal in log.meals)
    carbs = sum(meal.total_macros.carbs for meal in log.meals)
    fat = sum(meal.total_macros.fat for meal in log.meals)

    from src.integrations.diet.models import Macros
    return Macros(calories=calories, protein=protein, carbs=carbs, fat=fat)

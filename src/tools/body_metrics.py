import structlog
from langchain_core.tools import tool

from src.integrations.diet import client
from src.integrations.diet.exceptions import DietIntegrationError
from src.integrations.diet.models import BodyMetric

logger = structlog.get_logger(__name__)

@tool(description=(
    "Retrieve all historical body composition measurements: weight, body fat (kg), "
    "muscle mass, BMI, BMR, visceral fat, and metabolic age. "
    "Use when the user asks about their weight, body composition, fitness progress, "
    "or trends over time. Returns all recorded entries sorted by date."
))
def get_body_metrics() -> str:
    logger.info("Invoking get_body_metrics tool")
    try:
        metrics = client.get_body_metrics()
        return _parse_body_metrics(metrics)
    except DietIntegrationError as e:
        return f"Could not fetch body metrics: {e.message}"


def _parse_body_metrics(metrics: list[BodyMetric]) -> str:
    if not metrics:
        return "No body metrics found."

    metrics_strs = []
    for metric in metrics:
        metrics_strs.append(
            f"Date: {metric.date}, Weight: {metric.weightKg}kg, Body Fat: {metric.fatKg}kg, Muscle Mass: {metric.muscleMassKg}kg\n"
            f"BMI: {metric.bmi}, BMR: {metric.bmr}, Water Mass: {metric.waterMassKg}kg, Visceral Fat: {metric.visceralFat}\n"
            f"Bone Mass: {metric.boneMassKg}kg, Fat Free Mass: {metric.fatFreeKg}kg, Metabolic Age: {metric.metabolicAge}"
        )
    return "\n".join(metrics_strs)
from langchain_core.tools import tool

from src.integrations.diet.dietapp import DietAppClient
from src.integrations.diet.models import BodyMetric

_client = DietAppClient()

@tool(description="Returns a list of body metrics to track diet and workout progress")
def get_body_metrics() -> str:
    metrics = _client.get_body_metrics()
    return _parse_body_metrics(metrics)


def _parse_body_metrics(metrics: list[BodyMetric]) -> str:
    if not metrics:
        return "No body metrics found."

    metrics_strs = []
    for metric in metrics:
        metrics_strs.append(
            f"Date: {metric.date}, Weight: {metric.weightKg}kg, Body Fat: {metric.fatKg}%, Muscle Mass: {metric.muscleMassKg}kg\n"
            f"BMI: {metric.bmi}, BMR: {metric.bmr}, Water mass: {metric.waterMassKg}kg, Visceral Fat: {metric.visceralFat},\n"
            f"Bone Mass: {metric.boneMassKg}kg, Fat Free Mass: {metric.fatFreeKg}kg, Metabolic Age: {metric.metabolicAge}\n"
        )
    return "\n".join(metrics_strs)
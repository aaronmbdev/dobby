import httpx
from datetime import datetime

from openai.types.fine_tuning.jobs.fine_tuning_job_checkpoint import Metrics

from src.config.settings import settings
from src.integrations.diet.exceptions import DietIntegrationError
from src.integrations.diet.models import DayLog, Macros, Meal, Food


class DietAppClient:
    def __init__(self):
        self.profile_id = "a7c7c256-fb0c-4b5e-96bc-1f3b2d82fcd1"
        self.client = httpx.Client(
            base_url=settings.diet_url,
            headers={
                "Content-Type": "application/json",
            },
            follow_redirects=True,
        )

    def get_daily_log(self, date: str = None) -> DayLog:
        if date is None:
            date = datetime.today().strftime('%Y-%m-%d')
        endpoint = f"/api/daily-logs"
        try:
            data = self._make_get_request(endpoint, {"profileId": self.profile_id, "date": date})
            target = Macros(**data["target"])
            meals = [
                Meal(
                    foods=[
                        Food(
                            name=food["name"],
                            grams=food["grams"],
                            macros=Macros(**food["macros"])
                        )
                        for food in meal["foods"]
                    ],
                    total_macros=Macros(**meal["total_macros"])
                )
                for meal in data["meals"]
            ]
            return DayLog(
                date=data["date"],
                target=target,
                meals=meals
            )
        except httpx.HTTPError as e:
            raise DietIntegrationError(f"Error fetching daily log: {e}") from e


    def get_body_metrics(self) -> list[Metrics]:
        endpoint = f"/api/body-metrics"
        try:
            data = self._make_get_request(endpoint, {"profileId": self.profile_id})
            metrics = data.get("metrics")
            if not metrics:
                raise DietIntegrationError("No body metrics found for the given profile.")
            return [Metrics(**metric) for metric in metrics]
        except httpx.HTTPError as e:
            raise DietIntegrationError(f"Error fetching body metrics: {e}") from e


    def _make_get_request(self, url: str, params: dict) -> dict:
        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
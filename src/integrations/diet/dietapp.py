import httpx
from datetime import datetime
from src.config.settings import settings
from src.integrations.diet.exceptions import DietIntegrationError


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

    def get_app_health(self):
        try:
            return self._make_get_request("/api/health", {})
        except httpx.HTTPError as e:
            raise DietIntegrationError(f"Error fetching health: {e}") from e


    def get_daily_log(self, from_date: str = None, to_date: str = None):
        if from_date is None or to_date is None:
            from_date = datetime.today().strftime('%Y-%m-%d')
            to_date = datetime.today().strftime('%Y-%m-%d')
        endpoint = f"/api/daily-logs"
        try:
            return self._make_get_request(endpoint, {"profileId": self.profile_id, "date": to_date})
        except httpx.HTTPError as e:
            raise DietIntegrationError(f"Error fetching daily log: {e}") from e


    def get_body_metrics(self):
        endpoint = f"/api/body-metrics"
        try:
            return self._make_get_request(endpoint, {"profileId": self.profile_id})
        except httpx.HTTPError as e:
            raise DietIntegrationError(f"Error fetching body metrics: {e}") from e


    def _make_get_request(self, url: str, params: dict) -> httpx.Response:
        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
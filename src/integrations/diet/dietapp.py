import httpx

from src.config.settings import settings
from src.integrations.diet.exceptions import DietIntegrationError


class DietAppClient:
    def __init__(self):
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

    def log_meal(self, user_id: str, meal_data: dict):
        # Placeholder for API call to log a meal
        pass

    def get_nutrition_summary(self, user_id: str):
        # Placeholder for API call to get nutrition summary
        pass

    def _make_get_request(self, url: str, params: dict) -> httpx.Response:
        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
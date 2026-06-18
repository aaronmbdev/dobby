import httpx

from src.config.settings import settings


class HomeAssistantClient:

    def __init__(self):

        self.client = httpx.Client(
            base_url=settings.homeassistant_url,
            headers={
                "Authorization":
                    f"Bearer {settings.homeassistant_token}",
                "Content-Type": "application/json",
            },
            follow_redirects=True,
        )


    def fridge_door_open(
        self,
    ) -> bool:
        response = self.client.get(
            "/api/states/binary_sensor.frigorifico_fridge_door"
        )
        response.raise_for_status()
        response = response.json()
        return response["state"] == "on"
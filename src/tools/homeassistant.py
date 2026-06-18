from langchain.tools import tool

from src.integrations.homeassistant import HomeAssistantClient

_client = HomeAssistantClient()


@tool(description="Return 'open' or 'closed' indicating whether the fridge door is open.")
def is_fridge_open() -> str:
    return "open" if _client.fridge_door_open() else "closed"
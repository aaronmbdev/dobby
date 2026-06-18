from langchain.tools import tool
from src.integrations.homeassistant import HomeAssistantClient


@tool(description="Return 'open' or 'closed' indicating whether the fridge door is open.")
def is_fridge_open() -> str:
    client = HomeAssistantClient()
    return "open" if client.fridge_door_open() else "closed"
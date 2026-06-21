from src.tools.daily_food_log import get_daily_food_log
from src.tools.homeassistant import is_fridge_open
from src.tools.memory import remember, recall

TOOLS = [
    is_fridge_open,
    remember,
    recall,
    get_daily_food_log
]
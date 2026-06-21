from src.tools.body_metrics import get_body_metrics
from src.tools.goals import abandon_goal, complete_goal, create_goal, list_goals
from src.tools.daily_food_log import get_daily_food_log
from src.tools.finances import (
    get_accounts,
    get_financial_health,
    get_investment_funds,
    get_monthly_report,
    get_net_worth_history,
    get_stocks,
)
from src.tools.homeassistant import is_fridge_open
from src.tools.memory import remember, recall

TOOLS = [
    # home
    is_fridge_open,
    # memory
    remember,
    recall,
    # diet
    get_body_metrics,
    get_daily_food_log,
    # finances
    get_accounts,
    get_stocks,
    get_investment_funds,
    get_net_worth_history,
    get_financial_health,
    get_monthly_report,
    # goals
    create_goal,
    list_goals,
    complete_goal,
    abandon_goal,
]
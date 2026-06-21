from src.tools.body_metrics import get_body_metrics
from src.tools.can_i_afford import can_i_afford_a_phone, can_i_afford_a_car
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
from src.tools.calendar import (
    get_daily_agenda,
    get_weekly_agenda,
    search_calendar_events,
    create_calendar_event,
    update_calendar_event,
    delete_calendar_event,
)

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
    # calendar
    get_daily_agenda,
    get_weekly_agenda,
    search_calendar_events,
    create_calendar_event,
    update_calendar_event,
    delete_calendar_event,
    can_i_afford_a_phone,
    can_i_afford_a_car,
]
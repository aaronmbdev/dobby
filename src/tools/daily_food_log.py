from langchain_core.tools import tool

from src.integrations.diet.dietapp import DietAppClient
from src.integrations.diet.models import Macros

_client = DietAppClient()

@tool(
    description="Get the daily meal log for a specific date. If no date is provided, it will return today's log. Date must be in the format YYYY-MM-DD.")
def get_daily_food_log(date: str = None) -> str:
    data = _client.get_daily_log(date)
    target_macros = _parse_macros(data.target)
    meals = _parse_meals(data.meals)
    return f"""
    Daily Log for {date}:
    Target Macros: {target_macros}
    Meals:
    {meals}
    """


def _parse_macros(macros: Macros) -> str:
    return f"Calories: {macros.calories}, Protein: {macros.protein}g, Carbs: {macros.carbs}g, Fat: {macros.fat}g"


def _parse_meals(meals: list) -> str:
    meal_strs = []
    for meal in meals:
        meal_macros = _parse_macros(meal.total_macros)
        foods_str = "\n".join([f"  - {food.name}: {food.grams}g, { _parse_macros(food.macros)}" for food in meal.foods])
        meal_strs.append(f"Meal:\n{foods_str}\nTotal Macros: {meal_macros}")
    return "\n\n".join(meal_strs)
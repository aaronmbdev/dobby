import structlog
from langchain_core.tools import tool

from src.integrations.diet import client
from src.integrations.diet.exceptions import DietIntegrationError
from src.integrations.diet.models import Macros

logger = structlog.getLogger(__name__)

@tool(description=(
    "Get the meal-by-meal food log for a specific date, including each food item, "
    "its weight in grams, macros (calories, protein, carbs, fat), and the daily targets. "
    "Use when the user asks what they ate, their macro intake, or whether they hit their goals. "
    "Defaults to today if no date is provided. Date must be YYYY-MM-DD."
    "Each day should have at least 3 or 4 meals, if it has less, user probably skipped the meal or went to a restaurant"
))
def get_daily_food_log(date: str = None) -> str:
    logger.info("Invoking get_daily_food_log tool")
    try:
        data = client.get_daily_log(date)
        target_macros = _parse_macros(data.target)
        meals = _parse_meals(data.meals)
        return f"Daily Log for {data.date}:\nTarget Macros: {target_macros}\nMeals:\n{meals}"
    except DietIntegrationError as e:
        return f"Could not fetch daily food log: {e.message}"


def _parse_macros(macros: Macros) -> str:
    return f"Calories: {macros.calories}, Protein: {macros.protein}g, Carbs: {macros.carbs}g, Fat: {macros.fat}g"


def _parse_meals(meals: list) -> str:
    meal_strs = []
    for meal in meals:
        meal_macros = _parse_macros(meal.total_macros)
        foods_str = "\n".join([f"  - {food.name}: {food.grams}g, { _parse_macros(food.macros)}" for food in meal.foods])
        meal_strs.append(f"Meal:\n{foods_str}\nTotal Macros: {meal_macros}")
    return "\n\n".join(meal_strs)
from dataclasses import dataclass


@dataclass(frozen=True)
class BodyMetric:
    id: str
    date: str
    weightKg: float
    waterMassKg: float
    muscleMassKg: float
    fatKg: float
    boneMassKg: float
    fatFreeKg: float
    visceralFat: int
    bmr: int
    metabolicAge: int
    bmi: float
    notes: str
    createdAt: str


@dataclass(frozen=True)
class Macros:
    calories: int
    protein: int
    carbs: int
    fat: int


@dataclass(frozen=True)
class Meal:
    """
    Rerpresents a meal with a set of foods and the total macros for that meal
    """
    foods: list[Food]
    total_macros: Macros

@dataclass(frozen=True)
class Food:
    """
    Represents a key ingredient of a full meal with its name and macros
    """
    name: str
    grams: int
    macros: Macros

@dataclass(frozen=True)
class DayLog:
    """
    Complete report of a day of intake
    """
    date: str
    target: Macros
    meals: list[Meal]
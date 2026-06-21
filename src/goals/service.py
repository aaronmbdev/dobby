from src.goals.models import Goal
from src.goals.repository import GoalRepository


class GoalService:

    def __init__(self) -> None:
        self.repository = GoalRepository()

    def create(
        self,
        title: str,
        domain: str,
        target: str,
        deadline: str | None = None,
        notes: str | None = None,
    ) -> Goal:
        return self.repository.create(title, domain, target, deadline, notes)

    def list_active(self) -> list[Goal]:
        return self.repository.list_active()

    def complete(self, goal_id: int) -> bool:
        return self.repository.update_status(goal_id, "completed")

    def abandon(self, goal_id: int) -> bool:
        return self.repository.update_status(goal_id, "abandoned")

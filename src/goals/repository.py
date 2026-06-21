from sqlalchemy import select

from src.goals.models import Goal
from src.memory.database import SessionLocal


class GoalRepository:

    def create(
        self,
        title: str,
        domain: str,
        target: str,
        deadline: str | None,
        notes: str | None,
    ) -> Goal:
        with SessionLocal() as session:
            goal = Goal(title=title, domain=domain, target=target, deadline=deadline, notes=notes)
            session.add(goal)
            session.commit()
            session.refresh(goal)
            return goal

    def list_active(self) -> list[Goal]:
        with SessionLocal() as session:
            result = session.execute(select(Goal).where(Goal.status == "active"))
            return list(result.scalars().all())

    def update_status(self, goal_id: int, status: str) -> bool:
        with SessionLocal() as session:
            goal = session.get(Goal, goal_id)
            if not goal:
                return False
            goal.status = status
            session.commit()
            return True

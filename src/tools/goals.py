from langchain_core.tools import tool

from src.goals.service import GoalService

_service = GoalService()


@tool(description=(
    "Save a new personal goal the user wants to track. "
    "Use when the user sets a target or intention they want to work towards. "
    "domain must be one of: health, finances, diet, general. "
    "target should describe what success looks like in plain language. "
    "deadline is optional, format YYYY-MM-DD."
))
def create_goal(
    title: str,
    domain: str,
    target: str,
    deadline: str = None,
    notes: str = None,
) -> str:
    goal = _service.create(title, domain, target, deadline, notes)
    return f"Goal saved (id={goal.id}): {goal.title}"


@tool(description=(
    "List all active goals with their IDs, domains, targets, and deadlines. "
    "Use when the user asks about their goals, what they're working towards, "
    "or before completing or abandoning a goal to find the right ID."
))
def list_goals() -> str:
    goals = _service.list_active()
    if not goals:
        return "No active goals."
    lines = []
    for g in goals:
        line = f"[id={g.id}] ({g.domain}) {g.title} — {g.target}"
        if g.deadline:
            line += f" | due {g.deadline}"
        if g.notes:
            line += f" | {g.notes}"
        lines.append(line)
    return "\n".join(lines)


@tool(description=(
    "Mark a goal as completed. Use when the user confirms they have achieved a goal. "
    "Always confirm with the user before calling this. "
    "Call list_goals first if you don't have the goal ID."
))
def complete_goal(goal_id: int) -> str:
    if _service.complete(goal_id):
        return f"Goal {goal_id} marked as completed. Well done!"
    return f"Goal {goal_id} not found."


@tool(description=(
    "Mark a goal as abandoned. Use when the user decides to drop a goal they no longer want to pursue. "
    "Always confirm with the user before calling this. "
    "Call list_goals first if you don't have the goal ID."
))
def abandon_goal(goal_id: int) -> str:
    if _service.abandon(goal_id):
        return f"Goal {goal_id} marked as abandoned."
    return f"Goal {goal_id} not found."

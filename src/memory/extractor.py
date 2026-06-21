import structlog
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.config.settings import settings
from src.tools.memory import memory_service

logger = structlog.get_logger(__name__)


class _ExtractionResult(BaseModel):
    facts: list[str]


_llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    model=settings.openai_model,
    temperature=0,
).with_structured_output(_ExtractionResult)

_SYSTEM = SystemMessage(content="""
You are a memory extraction system for a personal AI assistant.

Given a conversation turn (user message + assistant response), extract facts about the user worth remembering long-term.

Rules:
- Only extract facts ABOUT THE USER — not general knowledge or assistant actions
- Only extract lasting information: preferences, goals, habits, relationships, health baselines, financial patterns
- Do NOT extract transient queries ("user asked about X today")
- Do NOT extract obvious or generic facts ("user has a bank account")
- Return an empty list if nothing in this turn is worth remembering
- Each fact must be a single, self-contained sentence

Good examples:
- "User is lactose intolerant"
- "User's gym is called Holmes Place"
- "User's monthly savings goal is €500"
- "User prefers tracking macros over just calories"
- "User dislikes meal prepping on weekdays"

Bad examples:
- "User asked about their bank balance" (transient)
- "User has finances" (obvious)
- "The assistant checked the fridge" (not about the user)
""")


def extract_and_save(user_message: str, assistant_response: str) -> None:
    try:
        result = _llm.invoke([
            _SYSTEM,
            HumanMessage(content=f"User: {user_message}\nAssistant: {assistant_response}"),
        ])
        for fact in result.facts:
            logger.info("saving extracted memory", fact=fact)
            memory_service.save(fact)
    except Exception:
        logger.exception("memory extraction failed")

from src.llm.openai import LLMClient


def answer_node(state: dict):
    llm = LLMClient()
    last_message = state["messages"][-1]["content"]

    response = llm.chat(last_message)

    return {
        "response": response
    }
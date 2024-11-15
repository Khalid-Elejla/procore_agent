# states.py
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
import operator

class GraphState(TypedDict):
    query: str
    messages: Annotated[list[AnyMessage], operator.add]

def where_to_go(state):
    messages = state['messages']
    last_message = messages[-1]
    if "function_call" in last_message.additional_kwargs:
        return "continue"
    else:
        return "end"

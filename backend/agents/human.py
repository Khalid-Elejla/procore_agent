from langchain_anthropic import ChatAnthropic
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.prebuilt import create_react_agent, InjectedState
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated, Literal
import logging
from typing import Dict, Any

def human(
    state: Dict[str, Any]#, config
) -> Command[Literal["api_handler", "human"]]:
    """A node for collecting user input."""
    logging.debug(f"VVVVVV: VVVVVVV")
    user_input = interrupt(value="Ready for user input.")
    
    logging.debug(f"AAAAAAAAAAAAAAA: {user_input}")
    # identify the last active agent
    # (the last active node before returning to human)
    # langgraph_triggers = config["metadata"]["langgraph_triggers"]
    # if len(langgraph_triggers) != 1:
    #     raise AssertionError("Expected exactly 1 trigger in human node")

    # # active_agent = langgraph_triggers[0].split(":")[1]

    return Command(
        update={
            "messages": [
                {
                    "role": "human",
                    "content": user_input,
                }
            ]
        },
        goto='api_handler',
    )

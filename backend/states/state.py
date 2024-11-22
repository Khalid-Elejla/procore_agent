# states.py
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
import operator
from langgraph.graph import START, StateGraph, END
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

def router(state):
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return END
    return "continue"

# Define the edges in the agent graph
def pass_review(state: AgentGraphState):
    review_list = state["router_response"]
    if review_list:
        review = review_list[-1]
    else:
        review = "No review"

    if review != "No review":
        if isinstance(review, HumanMessage):
            review_content = review.content
        else:
            review_content = review
        
        review_data = json.loads(review_content)
        next_agent = review_data["next_agent"]
    else:
        next_agent = "end"

    return next_agent
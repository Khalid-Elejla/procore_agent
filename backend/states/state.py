# states.py

from typing import TypedDict, Annotated, List, Tuple
from langchain_core.messages import AnyMessage
import operator
from langgraph.graph import START, StateGraph, END
import json

class PlanStep(TypedDict):
  step: int
  action: str
  agent: str

class AgentResponse(TypedDict):
  agent: str
  response: str

class AgentState(TypedDict):
  command: str
  agent: str
  messages: Annotated[List[AnyMessage], operator.add]

class GraphState(TypedDict):
  query: str
  plan: List[PlanStep]
  # current_task: AgentState
  feedback:Annotated[List[AgentResponse], operator.add]
  messages: Annotated[List[AnyMessage], operator.add]
  # sql_agent_messages: Annotated[List[AnyMessage], operator.add]


class AgentGraphState(TypedDict):
    query: str
    planner_messages: Annotated[list[AnyMessage], operator.add]
    router_messages: Annotated[list[AnyMessage], operator.add]
    sql_agent_messages: Annotated[list[AnyMessage], operator.add]

    messages: Annotated[list[AnyMessage], operator.add]

    # router_response: Annotated[list, add_messages]
    router_response: Annotated[List[Tuple[str, str]], operator.add]
    planner_response: Annotated[List[AnyMessage], operator.add]
    sql_agent_response: Annotated[List[AnyMessage], operator.add]

    final_Answer: Annotated[List[AnyMessage], operator.add]



# def where_to_go(state):
#     messages = state['messages']
#     last_message = messages[-1]
#     if "success" in last_message.content["status"]:
#         return END
#     elif "failure" in last_message.content["status"]:
#         return "router"
#     else:
#         return "reviewer error"
def where_to_go(state):
  messages = state['messages']
  last_message = messages[-1]

  try:
      # Parse the JSON content
      content = json.loads(last_message.content)

      # Access the status inside the "review" key
      status = content["review"]["status"]

      if "success" in status:
          return END
      elif "failure" in status:
          return "router"
      else:
          return "reviewer error"
  except json.JSONDecodeError:
      # Handle the case where the content is not valid JSON
      return "reviewer error"
  except KeyError:
      # Handle missing keys in the JSON
      return "reviewer error"
# def where_to_go(state):
#     messages = state['messages']
#     last_message = messages[-1]
#     if "function_call" in last_message.additional_kwargs:
#         return "continue"
#     else:
#         return "end"

# def router(state):
#     # This is the router
#     messages = state["messages"]
#     last_message = messages[-1]
#     if "FINAL ANSWER" in last_message.content:
#         # Any agent decided the work is done
#         return END
#     return "continue"

# def router(state):
#     # This is the router
#     messages = state["messages"]
#     last_message = messages[-1]
#     if "planner" in last_message.content["next_agent"]:
#         return "planner"
#     elif "web_scraper" in last_message.content["next_agent"]:
#         return "web_scraper"
#     elif "sql_agent" in last_message.content["next_agent"]:
#         return "sql_agent"
#     elif "reviewer" in last_message.content["next_agent"]:
#         return "reviewer"
#     else:
#         return "router_error"

def route(state: dict) -> str:
  """
  Routes to the next agent based on the last message in the conversation state.

  Args:
      state (dict): Current state containing messages and other information

  Returns:
      str: Name of the next agent to execute or 'router_error' if routing fails
  """
  try:
      # Get the last message from the state
      messages = state.get("messages", [])

      if not messages:
          return "planner"  # Default to planner if no messages

      last_message = messages[-1]

      # Extract the next_agent from the last message
      if hasattr(last_message, 'content'):
          # Handle different message content formats
          if isinstance(last_message.content, dict):
              next_agent = last_message.content.get("next_agent", "")
          elif isinstance(last_message.content, str):
              # Try to parse JSON if content is string
              try:
                  content_dict = json.loads(last_message.content)
                  next_agent = content_dict.get("next_agent", "")
              except json.JSONDecodeError:
                  next_agent = last_message.content
          else:
              return "router_error"
      else:
          return "router_error"

      # Route to appropriate agent
      valid_agents = {
          "planner": "planner",
          "web_scraper": "web_scraper",
          "sql_agent": "sql_agent",
          "reviewer": "reviewer"
      }

      # Check if next_agent matches any valid agent (case insensitive)
      for agent_key, agent_value in valid_agents.items():
          if agent_key.lower() in str(next_agent).lower():
              return agent_value

      # If no valid agent found
      return "router_error"

  except Exception as e:
      print(f"Routing error: {str(e)}")
      return "router_error"
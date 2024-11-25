from ..models.openai_models import load_openai_model  # Import the model loader

# from ..states.state import GraphState, where_to_go
from langchain_core.messages import HumanMessage
from ..prompts.prompts import get_router_system_message
from ..tools.utils_tools import get_search_tool
from ..tools.procore_toolset.projects_tools import create_project, get_projects, rename_project
from ..tools.procore_toolset.users_tools import create_user, get_users
from ..tools.database_tools import sync_users_from_procore

from typing import Dict, Any
import json

# Define search tool
search = get_search_tool()

# Initialize LLM using function from openai_models.py
llm = load_openai_model()
# users_tools=[create_user, get_users]
# projects_tools=[create_project, get_projects, rename_project]
# database_tools=[sync_users_from_procore]
# tools = [search] + database_tools + projects_tools
# llm_with_tools = llm.bind_tools(tools)


# Define reasoner function to invoke LLM with the current state
# def RouterAgent(state):
#     query = state["query"]
#     messages = state["messages"]
#     plan=state["messages"]
#     feedback=state["feedback"]
#     sys_msg = get_router_system_message(plan=plan,feedback=feedback)
#     message = HumanMessage(content=query)
#     messages.append(message)
# #    result = [llm_with_tools.invoke([sys_msg] + messages)]
#     result = [llm.invoke([sys_msg] + messages)]
#     return {"messages": result}



# def RouterAgent(state: Dict[str, Any]) -> Dict[str, Any]:
#   """
#   Router agent that determines the next agent to handle the conversation.

#   Args:
#       state (Dict[str, Any]): Contains query, messages, plan, and feedback

#   Returns:
#       Dict[str, Any]: Contains updated messages and routing information
#   """
#   query = state["query"]
#   messages = state["messages"]
#   plan = state.get("plan", "No plan available yet")
# #  plan = json.dump(state["plan"])

#   feedback = state.get("feedback", "No feedback available yet")

#   # Get system message with plan and feedback
#   sys_msg = get_router_system_message(plan=plan, feedback=feedback)

#   # Add user query to messages
#   message = HumanMessage(content=query)
#   messages.append(message)

#   # Get LLM response
#   response = llm.invoke([sys_msg] + messages)
#   messages.append(response)

#   # Parse the JSON response
#   try:
#       routing_decision = json.loads(response.content)
#       return {
#           "messages": messages,
#           "next_agent": routing_decision["next_agent"],
#           "command": routing_decision["command"]
#       }
#   except json.JSONDecodeError:
#       # Fallback if response is not valid JSON
#       return {
#           "messages": messages,
#           "next_agent": "planner",  # Default to planner if parsing fails
#           "command": "Please provide a clear plan for the task"
#       }
  

def RouterAgent(state: Dict[str, Any]) -> Dict[str, Any]:
  """
  Router agent that determines the next agent to handle the conversation.

  Args:
      state (Dict[str, Any]): Contains query, messages, plan, and feedback

  Returns:
      Dict[str, Any]: Contains updated messages and routing information
  """
  query = state["query"]
  messages = state["messages"]

  # Handle the plan from PlannerAgent
  if isinstance(state.get("plan"), list):
      plan = json.dumps(state["plan"], indent=2)
  else:
      plan = state.get("plan")#, "No plan available yet")

  feedback = state.get("feedback")#, "No feedback available yet")

  # Get system message with plan and feedback
  sys_msg = get_router_system_message(plan=plan, feedback=feedback)

  # Add user query to messages
#   message = HumanMessage(content=query)
#   messages.append(message)

  # Get LLM response
  response = llm.invoke([sys_msg] + messages)
  messages.append(response)

  # Parse the JSON response
  try:
      routing_decision = json.loads(response.content)
      return {
          "messages": messages,
          "next_agent": routing_decision["next_agent"],
          "command": routing_decision["command"]
      }
  except json.JSONDecodeError:
      # Fallback if response is not valid JSON
      return {
          "messages": messages,
          "next_agent": "planner",  # Default to planner if parsing fails
          "command": "Please provide a clear plan for the task"
      }
from ..models.openai_models import load_openai_model  # Import the model loader

# from ..states.state import GraphState, where_to_go
from langchain_core.messages import HumanMessage
from ..prompts.prompts import get_reviewer_system_message
from ..tools.utils_tools import get_search_tool
from ..tools.procore_toolset.users_tools import create_user, get_users
from ..tools.database_tools import sync_users_from_procore

from typing import TypedDict, Annotated, List, Tuple


# Define search tool


# Initialize LLM using function from openai_models.py
llm = load_openai_model()
# users_tools=[create_user, get_users]
# llm_with_tools = llm.bind_tools(tools)


# # Define reasoner function to invoke LLM with the current state
# def ReviewerAgent(state):
#     query = state["query"]
#     messages = state["messages"]
#     last_message = state["messages"]
#     sys_msg = get_reviewer_system_message()
#     message = HumanMessage(content=query)
#     messages.append(message)
#     result = [llm.invoke([sys_msg] + messages)]
#     return {"messages": result}
def ReviewerAgent(state):
  query = state["query"]
  messages = state["messages"]

  # Corrected: Get the last message from messages
  last_message = messages[-1] if messages else None

  sys_msg = get_reviewer_system_message()
  message = HumanMessage(content=query)
  messages.append(message)

  # Pass only the relevant messages to the LLM
  if last_message:
      result = llm.invoke([sys_msg, last_message, message])
  else:
      result = llm.invoke([sys_msg, message])

  # Ensure result is a list of messages
  return {"messages": [result]}

# SQLAgent_tool = SQLAgent.as_tool(
#   arg_types={"query task": str},  # Change to accept a natural language query
#   name="SQL Agent",
#   description="This agent specializes in converting natural language queries into SQL statements. It is connected to the Procore users database and can efficiently retrieve the required data based on user input. Simply provide a natural language question, and the agent will craft the corresponding SQL query to fetch the relevant data table."
# )
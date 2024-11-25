from ..models.openai_models import load_openai_model  # Import the model loader

# from ..states.state import GraphState, where_to_go
from langchain_core.messages import HumanMessage
from ..prompts.prompts import get_sql_agent_system_message
from ..tools.utils_tools import get_search_tool
from ..tools.procore_toolset.users_tools import create_user, get_users
from ..tools.database_tools import sync_users_from_procore

from typing import TypedDict, Annotated, List, Tuple, Dict, Any

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


# # Initialize LLM using function from openai_models.py
# llm = load_openai_model()
# # users_tools=[create_user, get_users]
# database_tools=[sync_users_from_procore]
# tools = database_tools
# llm_with_tools = llm.bind_tools(tools)


# # Define reasoner function to invoke LLM with the current state
# def SQLAgent(state):
#     query = state["query"]
#     messages = state["messages"]
#     last_message = state["messages"]
#     sys_msg = get_sql_agent_system_message(dialect="SQLite", top_k=5)
#     message = HumanMessage(content=query)
#     messages.append(message)
#     result = [llm_with_tools.invoke([sys_msg] + messages)]
#     return {"messages": result}

# Initialize LLM using function from openai_models.py
llm = load_openai_model()
# users_tools=[create_user, get_users]


db = SQLDatabase.from_uri("sqlite:///backend\\procore_db.sqlite")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

langchain_sql_toolbox= toolkit.get_tools()
database_tools=[sync_users_from_procore] + langchain_sql_toolbox
tools = database_tools
llm_with_tools = llm.bind_tools(tools)




def SQLAgent(state):
  """
  SQL agent that executes database queries and returns results.
  """
  query = state["query"]
  # messages = state.get("messages", [])
  messages = state["messages"]


  # Create system message
  sys_msg = get_sql_agent_system_message(dialect="SQLite", top_k=5)

  # Add user query to messages
  message = HumanMessage(content=query)
  # current_messages = [sys_msg, message]

  try:
      # Get response from LLM with tools
      # response = llm_with_tools.invoke(current_messages)
      response = llm_with_tools.invoke([sys_msg] + messages)
      return {
    #       "messages": messages.append([response]),
          "messages": messages + [response],
          "feedback": [{2:"SQL query execution completed"}]
      }

  except Exception as e:
      error_msg = HumanMessage(content=f"Error executing SQL query: {str(e)}")
      return {
          "messages": messages + [error_msg],
          "feedback": [{2:"Error in SQL execution"}]
      }
# def SQLAgent(state):
#   """
#   SQL agent that executes database queries and returns results.
#   """
#   query = state["query"]
#   messages = state["messages"]

#   # Create system message
#   sys_msg = get_sql_agent_system_message(dialect="SQLite", top_k=5)

#   try:
#       # Get response from LLM with tools
#       response = llm.invoke([sys_msg] + messages)
#       return {
#           "messages": messages + [response],  # Correct way to concatenate
#           "feedback": "SQL query execution completed"
#       }

#   except Exception as e:
#       error_msg = HumanMessage(content=f"Error executing SQL query: {str(e)}")
#       return {
#           "messages": messages + [error_msg],  # Also fix this line
#           "feedback": "Error in SQL execution"
#       }

#=================================================================================
# def SQLAgent(state: Dict[str, Any]) -> Dict[str, Any]:
#   """
#   SQL agent that executes database queries and returns results.
#   """
#   query = state["query"]
#   # messages = state.get("messages", [])
#   messages = state["messages"]


#   # Create system message
#   sys_msg = get_sql_agent_system_message(dialect="SQLite", top_k=5)

#   # Add user query to messages
#   message = HumanMessage(content=query)
#   current_messages = [sys_msg, message]

#   try:
#       # Get response from LLM with tools
#       response = llm_with_tools.invoke(current_messages)

#       return {
#           "messages": messages + [message, response],
#           "feedback": "SQL query execution completed"
#       }

#   except Exception as e:
#       error_msg = HumanMessage(content=f"Error executing SQL query: {str(e)}")
#       return {
#           "messages": messages + [message, error_msg],
#           "feedback": "Error in SQL execution"
#       }
#=============================================================================================================  
# def SQLAgent(state: Dict[str, Any]) -> Dict[str, Any]:
#   """
#   SQL agent that executes database queries and returns results.
#   """



#   query = state["query"]
#   messages = state.get("messages", [])  # Get messages with empty list default

#   # Create system message
#   sys_msg = get_sql_agent_system_message(dialect="SQLite", top_k=5)

#   # Add user query to messages
# #   message = HumanMessage(content=query)
# #   messages.append(message)

#   try:
#       # Get response from LLM with tools
#       response = llm_with_tools.invoke([sys_msg] + messages)

#       # Return the updated messages and response
#       return {
#           "messages": messages + [response],  # Append the response object, not a list
#           "feedback": "SQL query execution completed"
#       }

#   except Exception as e:
#       error_msg = HumanMessage(content=f"Error executing SQL query: {str(e)}")
#       return {
#           "messages": messages + [error_msg],
#           "feedback": "Error in SQL execution"
#       }

# SQLAgent_tool = SQLAgent.as_tool(
#   arg_types={"query task": str},  # Change to accept a natural language query
#   name="SQL Agent",
#   description="This agent specializes in converting natural language queries into SQL statements. It is connected to the Procore users database and can efficiently retrieve the required data based on user input. Simply provide a natural language question, and the agent will craft the corresponding SQL query to fetch the relevant data table."
# )
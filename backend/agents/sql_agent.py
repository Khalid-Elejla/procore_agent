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




# def SQLAgent(state):
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
 
#   # current_messages = [sys_msg, message]

#   try:
#       # Get response from LLM with tools
#       # response = llm_with_tools.invoke(current_messages)
#       response = llm_with_tools.invoke([sys_msg] + messages)
#       return {
#     #       "messages": messages.append([response]),
#           # "messages": messages + [response],
#           "messages": [response],
#           "feedback": [{2:"SQL query execution completed"}]
#       }

#   except Exception as e:
#       error_msg = HumanMessage(content=f"Error executing SQL query: {str(e)}")
#       return {
#           # "messages": messages + [error_msg],
#           "messages": [error_msg],
#           "feedback": [{2:"Error in SQL execution"}]
#       }
#=========================================================================
def parse_table_from_content(content: str) -> List[Dict]:
  """
  Helper function to parse table data from response content.
  Implement based on your specific output format.
  """
  # Implementation depends on how your SQL results are formatted
  # This is a placeholder - implement based on your needs
  try:
      # Add your parsing logic here
      pass
  except Exception as e:
      raise ValueError(f"Failed to parse table data: {str(e)}")
  
def SQLAgent(state: Dict[str, Any]) -> Dict[str, Any]:
  """
  SQL agent that executes database queries and returns structured results.
  """
  query = state["query"]
  messages = state["messages"]

  # Create system message
  sys_msg = get_sql_agent_system_message(dialect="SQLite", top_k=5)

  try:
      # Get response from LLM with tools
      response = llm_with_tools.invoke([sys_msg] + messages)

      # Extract SQL results from the response
      result_data = {
          "success": True,
          "data": None,
          "message": "",
          "error": None
      }

      # Parse the response to extract query results
      # Assuming the response contains SQL results in a structured format
      try:
          # Extract table data from response
          # This depends on how your llm_with_tools returns data
          if hasattr(response, 'additional_kwargs') and 'table_data' in response.additional_kwargs:
              result_data["data"] = response.additional_kwargs['table_data']
          elif hasattr(response, 'content'):
              # If no data but query executed successfully
              if "No records found" in response.content:
                  result_data["message"] = "Query executed successfully but returned no records"
                  result_data["data"] = []
              else:
                  # Try to parse table data from content
                  # This would depend on your specific output format
                  result_data["data"] = parse_table_from_content(response.content)

          return {
              "messages": [response],
            #   "feedback": [{
            #       "status": "success",
            #       "step": 2,
            #       "message": "SQL query execution completed",
            #       "result": result_data
            #   }]
              "feedback": [{
                  "agent": "sql_agent",
                  "response": f"{response.content}",
              }]
          }

      except Exception as parsing_error:
          result_data["success"] = False
          result_data["error"] = f"Error parsing query results: {str(parsing_error)}"
          return {
              "messages": [response],
            #   "feedback": [{
            #       "status": "error",
            #       "step": 2,
            #       "message": "Error parsing SQL results",
            #       "result": result_data
            #   }]
              "feedback": [{
                  "agent": "sql_agent",
                  "response": f"Error parsing SQL results",
              }]
          }

  except Exception as e:
      result_data = {
          "success": False,
          "data": None,
          "message": f"Error executing SQL query: {str(e)}",
          "error": str(e)
      }

      error_msg = HumanMessage(content=str(e))
      return {
          "messages": [error_msg],
          "feedback": [{
              "status": "error",
              "step": 2,
              "message": "SQL execution failed",
              "result": result_data
          }]
      }

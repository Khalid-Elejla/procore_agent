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


# Initialize LLM using function from openai_models.py
llm = load_openai_model()


db = SQLDatabase.from_uri("sqlite:///./backend/procore_db.sqlite")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

database_tools = toolkit.get_tools()
llm_with_tools = llm.bind_tools(database_tools)

#=========================================================================
  
# def SQLAgent(state: Dict[str, Any]) -> Dict[str, Any]:
#   """
#   SQL agent that executes database queries and returns structured results.
#   """
#   query = state["query"]
#   messages = state["messages"]
#   command=state["command"]
#   sql_agent_messages=state["sql_agent_messages"]


#   # Create system message
#   sys_msg = get_sql_agent_system_message(dialect="SQLite", top_k=20) #, command=command)


#   try:
#       response = llm_with_tools.invoke([sys_msg] + sql_agent_messages + [command])

#       tool_name=None
#       tool_args=None
      
#       feedback_message = f"{response.content}"
  
#       # Check if 'tool_calls' exists and is not empty at the top level
#       if hasattr(response, "tool_calls") and response.tool_calls:
#           tool_calls = response.tool_calls
#         #   feedback_message = f"{response.content}"

#           # Loop through all tool calls to append their details to the feedback message
#           for call in tool_calls:
#               tool_name = call.get("name")
#               tool_args = call.get("args")
              
#               if tool_name:
#                   feedback_message += f" calling the {tool_name} tool"
#               if tool_args:
#                   feedback_message += f" with the following arguments: {tool_args}"

#       return {
#           # "messages": [response],
#           "sql_agent_messages":[response],
#           "command": command,
#       #   "feedback": [{
#       #       "status": "success",
#       #       "step": 2,
#       #       "message": "SQL query execution completed",
#       #       "result": result_data
#       #   }]
#           "feedback": [{
#               "agent": "sql_agent",
#               "command":command,
#               "response": feedback_message,
#               # "response": f"{response.content}" + (f" calling the {tool_name} tool" if tool_name else "") + (f" with the following arguments: {tool_args}" if tool_args else ""),
#               "status": "Success",
#           }]
#       }

#   except Exception as e:
#       result_data = {
#           "success": False,
#           "data": None,
#           "message": f"Error executing SQL query: {str(e)}",
#           "error": str(e)
#       }

#       error_msg = HumanMessage(content=str(e))
#       return {
#           "sql_agent_messages":[error_msg],
#           "command": command,
#           # "messages": [error_msg],
#           "feedback": [{
#               "status": "error",
#               "step": 2,
#               "message": "SQL execution failed",
#               "result": result_data
#           }]
#       }

#======================================================================================================================================
# from typing import TypedDict, Dict, Optional
# import pandas as pd
# from states.state import SQLState

# def SQLAgent(state: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     SQL agent that executes database queries and returns structured results.
#     """
#     query = state["query"]
#     messages = state["messages"]
#     command = state["command"]
#     sql_agent_messages = state["sql_agent_messages"]

#     # Initialize SQL state if not exists
#     sql_state: SQLState = state.get("sql_state", {"tables": {}, "status": None})

#     # Create system message
#     sys_msg = get_sql_agent_system_message(dialect="SQLite", top_k=20)

#     try:
#         response = llm_with_tools.invoke([sys_msg] + sql_agent_messages + [command])
#         feedback_message = f"{response.content}"

#         # Handle tool calls and store results
#         if hasattr(response, "tool_calls") and response.tool_calls:
#             tool_calls = response.tool_calls

#             for call in tool_calls:
#                 tool_name = call.get("name")
#                 tool_args = call.get("args")

#                 # Add tool call details to feedback
#                 if tool_name:
#                     feedback_message += f" calling the {tool_name} tool"
#                 if tool_args:
#                     feedback_message += f" with the following arguments: {tool_args}"

#                 # If the tool call returns data, store it in sql_state
#                 if tool_name == "sql_db_query":
#                     # Assuming the tool execution returns a DataFrame
#                     # You'll need to adapt this based on your actual tool implementation
#                     result_df = execute_tool_call(tool_name, tool_args)  # This is a placeholder

#                     # Extract table name from the query/args
#                     # This is a simplified example - you might need more sophisticated parsing
#                     table_name = extract_table_name(tool_args)  # This is a placeholder

#                     # Store the result in sql_state
#                     sql_state["tables"][table_name] = {
#                         "data": result_df,
#                         "table_name": table_name,
#                         "comment": f"Query result from {command}"
#                     }

#         sql_state["status"] = "success"

#         return {
#             "sql_agent_messages": [response],
#             "command": command,
#             "sql_state": sql_state,  # Add the SQL state to the return
#             "feedback": [{
#                 "agent": "sql_agent",
#                 "command": command,
#                 "response": feedback_message,
#                 "status": "Success",
#             }]
#         }

#     except Exception as e:
#         sql_state["status"] = "error"
#         error_msg = HumanMessage(content=str(e))

#         return {
#             "sql_agent_messages": [error_msg],
#             "command": command,
#             "sql_state": sql_state,
#             "feedback": [{
#                 "status": "error",
#                 "step": 2,
#                 "message": "SQL execution failed",
#                 "result": {
#                     "success": False,
#                     "data": None,
#                     "message": f"Error executing SQL query: {str(e)}",
#                     "error": str(e)
#                 }
#             }]
#         }

# # Placeholder functions that you'll need to implement
# def execute_tool_call(tool_name: str, tool_args: dict) -> pd.DataFrame:
#     """
#     Execute the tool call and return the result as a DataFrame
#     """
#     # Implement based on your actual tool implementation
#     pass

# def extract_table_name(tool_args: dict) -> str:
#     """
#     Extract table name from tool arguments
#     """
#     # Implement based on your query parsing needs
#     pass

#=========================================================================================================================================

from typing import TypedDict, Dict, Optional
import pandas as pd
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.schema import SystemMessage, HumanMessage
from ..states.state import TableState
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


#=============================================================================
def parse_agent_messages(messages):
    """
    Parses and processes messages in a conversation.

    Args:
        messages (list): List of LangChain message objects 
                        (HumanMessage, AIMessage, ToolMessage).
    """
    for msg in messages:
        # User (HumanMessage)
        if isinstance(msg, HumanMessage):
            print(f"User: {msg.content}\n")

        # AI Agent (AIMessage)
        elif isinstance(msg, AIMessage):
            if 'tool_calls' in msg.additional_kwargs and msg.additional_kwargs['tool_calls']:
                print("Agent is deciding to use tools...\n")
                for tool_call in msg.additional_kwargs['tool_calls']:
                    tool_name = tool_call['function']['name']
                    arguments = tool_call['function']['arguments']
                    print(f"Agent calls tool: {tool_name} with arguments {arguments}\n")
            else:
                print(f"Agent's Final Response:\n{msg.content}\n")

        # Tool Response (ToolMessage)
        elif isinstance(msg, ToolMessage):
            tool_name = msg.name
            print(f"Tool [{tool_name}] Response:\n{msg.content}\n")

        # Unknown Message Type
        else:
            print(f"Unknown message type: {msg}\n")

#=============================================================================
def SQLAgent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    SQL agent that executes database queries and returns structured results using SQLDatabaseToolkit.
    """
    query = state["query"]
    messages = state["messages"]
    command = state["command"]
    sql_agent_messages = state["sql_agent_messages"]

    # Initialize SQL state if not exists
    table_state : TableState = {}

    # Create system message
    sys_msg = get_sql_agent_system_message(dialect="SQLite", top_k=5)

    try:  

        # context_message = HumanMessage(content=f"""
        #     Previous interactions summary:
        #     - previous messages: {sql_agent_messages}
        #     - original command: {command}""")
        
        response = llm_with_tools.invoke([sys_msg] + [command]+ sql_agent_messages )
        # response = llm_with_tools.invoke([sys_msg] + [context_message])

        feedback_message = f"{response.content}"




        # parse_agent_messages(sql_agent_messages)
        if hasattr(response, "tool_calls") and response.tool_calls:
            tool_calls = response.tool_calls

            for call in tool_calls:
                tool_name = call.get("name")
                tool_args = call.get("args", {})

                # Add tool call details to feedback
                if tool_name:
                    feedback_message += f"\nCalling the {tool_name} tool"
                if tool_args:
                    feedback_message += f" with the following arguments: {tool_args}"

        # last_sql_agent_message = sql_agent_messages[-1] if sql_agent_messages else None
        # # # Handle different tool calls
        # # if hasattr(last_sql_agent_message, "tool_call_id") and last_sql_agent_message.tool_call_id:
        # if hasattr(last_sql_agent_message, "type") and last_sql_agent_message.type=="tool":
        #     tool_name = last_sql_agent_message.name

        #     table_state : TableState= {
        #         "data": "query_result",
        #         "table_name": "table_nnnnnnnnnnnnnn",
        #         "comment": f"Query result from: ",#{tool_args.get('query')}",
        #         "schema": "nnnnnnnnnnnn",#sql_state["tables"].get(table_name, {}).get("schema")
        #         "status": "success"
        #     }                    
        #     if tool_name == "sql_db_query":
        #         query_result=pd.eval(last_sql_agent_message.content)    

        #         table_state : TableState= {
        #             "data": "query_result",
        #             "table_name": "table_name",
        #             "comment": f"Query result from: ",#{tool_args.get('query')}",
        #             "schema": "schemea",#sql_state["tables"].get(table_name, {}).get("schema")
        #             "status": "success"
        #         }
        #     else:
        #         table_state: TableState= {
        #             "data": "query_result",
        #             "table_name": "table_name",
        #             "comment": f"Query result from: ",#{tool_args.get('query')}",
        #             "schema": "schemea",#sql_state["tables"].get(table_name, {}).get("schema")
        #             "status": "error"
        #         }

                # if tool_name == "sql_db_query":
                #     # Execute query and store results
                #     query_result = execute_tool_call(tool_name, tool_args)
                #     if isinstance(query_result, pd.DataFrame):
                #         # Try to extract table name from the query
                #         table_name = extract_table_name_from_query(tool_args.get("query", ""))
                #         if table_name:
                #             sql_state["tables"][table_name] = {
                #                 "data": query_result,
                #                 "table_name": table_name,
                #                 "comment": f"Query result from: {tool_args.get('query')}",
                #                 "schema": sql_state["tables"].get(table_name, {}).get("schema")
                #             }

        # sql_state["tables"]["table_name"] = {
        #     "data": "query_result",
        #     "table_name": "table_name",
        #     "comment": f"Query result from: ",#{tool_args.get('query')}",
        #     "schema": "schemea"#sql_state["tables"].get(table_name, {}).get("schema")
        # }
        # sql_state["status"] = "success"

        return {
            "messages": [response],
            "sql_agent_messages": [response],
            "command": command,
            "sql_state": [table_state],
            "feedback": [{
                "agent": "sql_agent",
                "command": command,
                "response": feedback_message,
                "status": "Success",
            }]
        }
    

    except Exception as e:
        # sql_state["status"] = "error"
        error_msg = HumanMessage(content=str(e))

        return {
            "sql_agent_messages": [error_msg],
            "command": command,
            # "sql_state": [table_state],
            "feedback": [{
                "status": "error",
                "step": 2,
                "message": "SQL execution failed",
                "result": {
                    "success": False,
                    "data": None,
                    "message": f"Error executing SQL query: {str(e)}",
                    "error": str(e)
                }
            }]
        }

# def extract_table_name_from_query(query: str) -> Optional[str]:
#     """
#     Extract table name from SQL query.
#     Basic implementation - you might want to make this more robust.
#     """
#     query = query.lower()
#     # Look for FROM clause
#     if "from" in query:
#         parts = query.split("from")[1].strip().split()
#         if parts:
#             # Remove any trailing clauses or whitespace
#             table_name = parts[0].strip(';').strip()
#             return table_name
#     return None

# def execute_tool_call(tool_name: str, tool_args: dict) -> Any:
#     """
#     Execute the tool call using SQLDatabaseToolkit.
#     This is a placeholder - you'll need to implement the actual tool execution
#     based on your setup.
#     """
#     # This should be implemented based on your actual toolkit setup
#     # Example implementation:
#     if tool_name == "list_tables":
#         return toolkit.get_tools()[0].run()  # Returns list of tables
#     elif tool_name == "schema":
#         return toolkit.get_tools()[1].run(tool_args)  # Returns schema info
#     elif tool_name == "sql_db_query":
#         return toolkit.get_tools()[3].run(tool_args["query"])  # Returns DataFrame
#     return None
from backend.tools.initialize_tools import initialize_api_tools
from ..models.openai_models import load_openai_model  # Import the model loader

# from ..states.state import GraphState, where_to_go
from langchain_core.messages import HumanMessage, AIMessage
from ..prompts.prompts import get_api_handler_system_message
from ..tools.utils_tools import get_search_tool


import json
from typing import Dict, Any
import logging
import streamlit as st


# Define search tool
# search = get_search_tool()


def APIHandlerAgent(state: Dict[str, Any]) -> Dict[str, Any]:


    # Initialize LLM using function from openai_models.py
    llm = load_openai_model()
    api_spec_file = 'procore_api_spec.json'
    overrides = {"servers": [{"url": "https://sandbox.procore.com"}]}

    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
    access_token = st.session_state.access_token

    tools=initialize_api_tools(access_token, api_spec_file, overrides)

    llm_with_tools = llm.bind_tools(tools)


    query = state["query"]
    messages = state["messages"]
    plan = state.get("plan", [])
    command = state["command"]
    feedback = state.get("feedback", [])
    # sql_agent_messages = state["sql_agent_messages"]
    # db_agent_feedback = state["db_agent_feedback"]

    sys_msg = get_api_handler_system_message()

    api_handler_prompt = f"""
  here is the user original query
  query: {query}

  - command to execute: {command}
  
  - feedback: {db_agent_feedback} + {sql_feedback_message}

  Here is the feedback provided by the agents:
  Feedback: {feedback}
  

  Here is documentation on the API:
  Base url: {procore_api_spec.servers[0]['url']}
  Endpoints: {procore_api_spec.endpoints}
  note that you can use the api call to get some messing values needed for the next api call

  """
    message = HumanMessage(content=api_handler_prompt)
    
    try:
        response = llm_with_tools.invoke([sys_msg, message])

        # Capture the model's response
        feedback_message = f"{response.content}"
        api_feedback_message += f"{response.content}"


        # If the response includes any tool calls, append them to feedback
        if hasattr(response, "tool_calls") and response.tool_calls:
            for call in response.tool_calls:
                tool_name = call.get("name")
                tool_args = call.get("args", {})

                if tool_name:
                    feedback_message += f"\nCalling the {tool_name} tool"
                    sql_feedback_message += f"\nCalling the {tool_name} tool"
                if tool_args:
                    feedback_message += f" with the following arguments: {tool_args}"
                    sql_feedback_message += f" with the following arguments: {tool_args}"

        # Build the return dictionary
        return_dict = {
            "messages": [response],
            "sql_agent_messages": [response],
            "command": command,
            "feedback": [
                {
                    "agent": "sql_agent",
                    "command": command,
                    "response": feedback_message,
                    "status": "Success",
                }
            ],
            "db_agent_feedback": [sql_feedback_message],
        }

        return return_dict

    except Exception as e:
        error_msg = HumanMessage(content=str(e))
        return {
            "sql_agent_messages": [error_msg],
            "command": command,
            "feedback": [
                {
                    "status": "error",
                    "step": 2,
                    "message": "SQL execution failed",
                    "result": {
                        "success": False,
                        "data": None,
                        "message": f"Error executing SQL query: {str(e)}",
                        "error": str(e),
                    },
                }
            ],
        }
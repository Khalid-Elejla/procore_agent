# main.py
from ..models.openai_models import load_openai_model  # Import the model loader
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition, ToolNode
from IPython.display import Image, display

from ..states.state import  route, GraphState, where_to_go
from langchain_core.messages import HumanMessage
# from ..prompts.prompts import get_reasoner_system_message
from ..tools.utils_tools import get_search_tool
from ..tools.procore_toolset.projects_tools import create_project, get_projects, rename_project
from ..tools.procore_toolset.users_tools import create_user, get_users
from ..tools.database_tools import sync_users_from_procore
# from ..agents.reasoner_agent import ReasonerAgent
from ..agents.planner_agent import PlannerAgent
from ..agents.router_agent import RouterAgent
from ..agents.sql_agent import SQLAgent
from ..agents.reviewer_agent import ReviewerAgent

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# import logging
# logging.basicConfig(level=logging.DEBUG)


# from pydantic import BaseModel
# from langchain_core.messages import (AnyMessage,)
# from typing import (Any,Union, Literal)

# def tools_condition(
#     state: Union[list[AnyMessage], dict[str, Any], BaseModel],
# ) -> Literal["tools", "__end__"]:
#         """Use in the conditional_edge to route to the ToolNode if the last message

#         has tool calls. Otherwise, route to the end.

#         Args:
#             state (Union[list[AnyMessage], dict[str, Any], BaseModel]): The state to check for
#                 tool calls. Must have a list of messages (MessageGraph) or have the
#                 "messages" key (StateGraph).

#         Returns:
#             The next node to route to.
#         """
#         if isinstance(state, list):
#             ai_message = state[-1]
#         elif isinstance(state, dict) and (messages := state.get("sql_agent_messages", [])):
#             ai_message = messages[-1]
#         elif messages := getattr(state, "sql_agent_messages", []):
#             ai_message = messages[-1]
#         else:
#             raise ValueError(f"No messages found in input state to tool_edge: {state}")
#         if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
#             return "tools"
#         return "__end__"



def build_graph():
    try:
        llm = load_openai_model()
        # logging.debug("Initializing SQLDatabaseToolkit...")
        db = SQLDatabase.from_uri("sqlite:///backend\\procore_db.sqlite")
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        # logging.debug("Fetching tools from toolkit...")
        langchain_sql_toolbox = toolkit.get_tools()
        # logging.debug(f"Tools fetched: {langchain_sql_toolbox}")

        database_tools = [sync_users_from_procore] + langchain_sql_toolbox

        # logging.debug(f"Final database tools: {database_tools}")

        builders = StateGraph(GraphState)

        builders.add_node("planner", PlannerAgent)
        builders.add_node("router", RouterAgent)
        builders.add_node("sql_agent", SQLAgent)
        builders.add_node("reviewer", ReviewerAgent)
        builders.add_node("sql_tools", ToolNode(database_tools))

        builders.add_edge(START, "planner")
        builders.add_edge("planner", "router")

        builders.add_conditional_edges("router", route)
        builders.add_conditional_edges(
            "sql_agent",
            tools_condition,
            {
                "tools": "sql_tools",
                "__end__": "router"
            }
        )
        builders.add_edge("sql_tools", "sql_agent")
   
        builders.add_edge("reviewer", END)

        react_graphs = builders.compile()
        # logging.debug("Graph built successfully!")
        return react_graphs
    except Exception as e:
        # logging.error(f"Error occurred in build_graph: {e}")
        raise

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

import logging




# def build_graph():

#     # Define search tool
#     search = get_search_tool()

#     # # Initialize LLM using function from openai_models.py
#     # llm = load_openai_model()
#     # users_tools=[create_user, get_users]
#     projects_tools=[create_project, get_projects, rename_project]
#     database_tools=[sync_users_from_procore]
#     tools=database_tools


#     # tools = [search] + projects_tools + SQLAgent_tool
#     # llm_with_tools = llm.bind_tools(tools)

#     # # Define reasoner function to invoke LLM with the current state
#     # def reasoner(state):
#     #     query = state["query"]
#     #     messages = state["messages"]
#     #     sys_msg = get_system_message()
#     #     message = HumanMessage(content=query)
#     #     messages.append(message)
#     #     result = [llm_with_tools.invoke([sys_msg] + messages)]
#     #     return {"messages": result}


#     # Build the state graph
#     builders = StateGraph(GraphState)
#     builders.add_node("planner", PlannerAgent)
#     builders.add_node("router", RouterAgent)
#     builders.add_node("sql_agent", SQLAgent)
#     builders.add_node("reviewer", ReviewerAgent)

#     #builders.add_node("reviewer")
#     builders.add_node("sql_tools", ToolNode(tools))
#     builders.add_conditional_edges("sql_agent", tools_condition, 
#                                          {
#           "tools": "sql_tools",  # Route to tools when tool calls are present
#           "__end__": "router"    # Route back to router when no tool calls
#       })
#     builders.add_edge("sql_tools", "sql_agent")

    
#     builders.add_edge(START, "planner")
#     builders.add_edge("planner", "router")
#     builders.add_edge("sql_agent", "router")
#     # builders.add_edge("web_scraper", "router")
#     builders.add_edge("reviewer", "router")

#     builders.add_conditional_edges("router", route)
    
    
#     builders.add_conditional_edges("reviewer", where_to_go)
    

#     # builders = StateGraph(GraphState)
#     # builders.add_node("reasoner", ReasonerAgent)
#     # builders.add_node("tools", ToolNode(tools))
#     # #builders.add_node("sql_agent", SQLAgent)

    
#     # builders.add_edge(START, "reasoner")
#     # builders.add_conditional_edges("reasoner", tools_condition)
    
#     # builders.add_edge("tools", "reasoner")
    


#     # builders.add_edge("sql_agent", "reasoner")
#     # builders.add_conditional_edges("reasoner", "sql_agent")

#     # Compile and visualize the graph
#     react_graphs = builders.compile()
#     # display(Image(react_graphs.get_graph(xray=True).draw_mermaid_png()))
#     return react_graphs

# # Call the function to build and display the graph
# build_graph()
#==========================================================================================
# def build_graph():
#   # Tool definitions


#   import logging

#   logging.basicConfig(level=logging.DEBUG)  # Set log level to DEBUG to see all logs

#   try:
#         db = SQLDatabase.from_uri("sqlite:///procore_db.sqlite")
#         logging.info("Successfully connected to the database.")
#   except Exception as e:
#         logging.error("Failed to connect to the database.", exc_info=True)

 

#   toolkit = SQLDatabaseToolkit(db=db)

#   langchain_sql_toolbox= toolkit.get_tools()
#   database_tools=[sync_users_from_procore] + langchain_sql_toolbox
  


#   projects_tools = [create_project, get_projects, rename_project]
#   # database_tools = [sync_users_from_procore]
#   tools = database_tools

#   # Build the state graph
#   builders = StateGraph(GraphState)

#   # Add nodes
#   builders.add_node("planner", PlannerAgent)
#   builders.add_node("router", RouterAgent)
#   builders.add_node("sql_agent", SQLAgent)
#   builders.add_node("reviewer", ReviewerAgent)

#   builders.add_node("sql_tools", ToolNode(tools))

#   # Add basic edges
#   builders.add_edge(START, "planner")
#   builders.add_edge("planner", "router")
#   # builders.add_edge("reviewer", "router")

#   # Add conditional edges for SQL agent and tools
#   builders.add_conditional_edges(
#       "sql_agent",
#       tools_condition,
#       {
#           "tools": "sql_tools",  # Route to tools when tool calls are present
#           "__end__": "router"    # Route back to router when no tool calls
#       }
#   )

#   # Add edge from tools back to SQL agent
#   builders.add_edge("sql_tools", "sql_agent")

#   # Add router conditional edges
#   builders.add_conditional_edges("router", route)

#   # Add reviewer conditional edges
# #   builders.add_conditional_edges("reviewer", where_to_go)
#   builders.add_edge("reviewer", END)

#   # Compile the graph
#   react_graphs = builders.compile()
#   return react_graphs
import logging

logging.basicConfig(level=logging.DEBUG)

def build_graph():

    try:
        llm = load_openai_model()
        logging.debug("Initializing SQLDatabaseToolkit...")
        db = SQLDatabase.from_uri("sqlite:///backend\\procore_db.sqlite")
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        logging.debug("Fetching tools from toolkit...")
        langchain_sql_toolbox = toolkit.get_tools()
        logging.debug(f"Tools fetched: {langchain_sql_toolbox}")

        database_tools = [sync_users_from_procore] + langchain_sql_toolbox

        logging.debug(f"Final database tools: {database_tools}")

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
        logging.debug("Graph built successfully!")
        return react_graphs
    except Exception as e:
        logging.error(f"Error occurred in build_graph: {e}")
        raise

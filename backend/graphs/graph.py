# main.py
from ..models.openai_models import load_openai_model  # Import the model loader
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition, ToolNode
from IPython.display import Image, display

from ..states.state import GraphState, router
from langchain_core.messages import HumanMessage
from ..prompts.prompts import get_reasoner_system_message
from ..tools.utils_tools import get_search_tool
from ..tools.procore_toolset.projects_tools import create_project, get_projects, rename_project
from ..tools.procore_toolset.users_tools import create_user, get_users
from ..tools.database_tools import sync_users_from_procore
from ..agents.reasoner_agent import ReasonerAgent
from ..agents.sql_agent import SQLAgent



def build_graph():

    # Define search tool
    search = get_search_tool()

    # # Initialize LLM using function from openai_models.py
    # llm = load_openai_model()
    # users_tools=[create_user, get_users]
    projects_tools=[create_project, get_projects, rename_project]
    database_tools=[sync_users_from_procore]
    tools = [search] + database_tools + projects_tools
    #llm_with_tools = llm.bind_tools(tools)

    # # Define reasoner function to invoke LLM with the current state
    # def reasoner(state):
    #     query = state["query"]
    #     messages = state["messages"]
    #     sys_msg = get_system_message()
    #     message = HumanMessage(content=query)
    #     messages.append(message)
    #     result = [llm_with_tools.invoke([sys_msg] + messages)]
    #     return {"messages": result}


    # Build the state graph
    builders = StateGraph(GraphState)
    builders.add_node("reasoner", ReasonerAgent)
    builders.add_node("tools", ToolNode(tools))
    #builders.add_node("sql_agent", SQLAgent)

    
    builders.add_edge(START, "reasoner")
    builders.add_conditional_edges("reasoner", tools_condition)
    
    builders.add_edge("tools", "reasoner")
    


    # builders.add_edge("sql_agent", "reasoner")
    # builders.add_conditional_edges("reasoner", "sql_agent")

    # Compile and visualize the graph
    react_graphs = builders.compile()
    # display(Image(react_graphs.get_graph(xray=True).draw_mermaid_png()))
    return react_graphs

# Call the function to build and display the graph
build_graph()

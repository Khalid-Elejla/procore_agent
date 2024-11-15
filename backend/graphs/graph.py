# from ..models.openai_models import load_openai_model  # Import the model loader
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langgraph.graph import START, StateGraph, END
# from langgraph.prebuilt import tools_condition, ToolNode
# from langchain_core.messages import HumanMessage, SystemMessage
# from IPython.display import Image, display

# from typing import Annotated
# from typing_extensions import TypedDict
# import operator
# import os

# from langchain_core.messages import AnyMessage

# def build_graph():

#     # Define search tool
#     search = TavilySearchResults(max_results=2,tavily_api_key=os.getenv("TAVILY_API_KEY"))

#     # Define graph state
#     class GraphState(TypedDict):
#         query: str
#         messages: Annotated[list[AnyMessage], operator.add]

#     # Initialize LLM using function from openai_models.py
#     llm = load_openai_model()
#     tools = [search,] # get_users, create_user, get_user_info_by_name, update_user]
#     llm_with_tools = llm.bind_tools(tools)

#     # Define reasoner function to invoke LLM with the current state
#     def reasoner(state):
#         query = state["query"]
#         messages = state["messages"]
#         sys_msg = SystemMessage(
#             content="You are an AI assistant specializing exclusively in Procore. Your role is to answer questions "
#                     "and provide assistance strictly on Procore-related topics. Politely decline to respond to any "
#                     "inquiries that are unrelated to Procore, and always keep responses focused, helpful, and accurate "
#                     "within your area of expertise."
#         )
#         message = HumanMessage(content=query)
#         messages.append(message)
#         result = [llm_with_tools.invoke([sys_msg] + messages)]
#         return {"messages": result}

#     # Define function to determine where to go next based on last message
#     def where_to_go(state):
#         messages = state['messages']
#         last_message = messages[-1]
#         if "function_call" in last_message.additional_kwargs:
#             return "continue"
#         else:
#             return "end"

#     # Build the state graph
#     builders = StateGraph(GraphState)
#     builders.add_node("reasoner", reasoner)
#     builders.add_node("tools", ToolNode(tools))
#     builders.add_edge(START, "reasoner")
#     builders.add_conditional_edges("reasoner", tools_condition)
#     builders.add_edge("tools", "reasoner")

#     # Compile and visualize the graph
#     react_graphs = builders.compile()
#     display(Image(react_graphs.get_graph(xray=True).draw_mermaid_png()))
#     return react_graphs

# # Call the function to build and display the graph
# build_graph()

# main.py
from ..models.openai_models import load_openai_model  # Import the model loader
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition, ToolNode
from IPython.display import Image, display

from ..states.state import GraphState, where_to_go
from langchain_core.messages import HumanMessage
from ..prompts.prompts import get_system_message
from ..tools.utils_tools import get_search_tool
from ..tools.procore_toolset.projects_tools import create_project, get_projects, rename_project
from ..tools.procore_toolset.users_tools import create_user, get_users


def build_graph():
    # Define search tool
    search = get_search_tool()

    # Initialize LLM using function from openai_models.py
    llm = load_openai_model()
    users_tools=[create_user, get_users]
    projects_tools=[create_project, get_projects, rename_project]
    tools = [search] + users_tools + projects_tools
    llm_with_tools = llm.bind_tools(tools)

    # Define reasoner function to invoke LLM with the current state
    def reasoner(state):
        query = state["query"]
        messages = state["messages"]
        sys_msg = get_system_message()
        message = HumanMessage(content=query)
        messages.append(message)
        result = [llm_with_tools.invoke([sys_msg] + messages)]
        return {"messages": result}

    # Build the state graph
    builders = StateGraph(GraphState)
    builders.add_node("reasoner", reasoner)
    builders.add_node("tools", ToolNode(tools))
    builders.add_edge(START, "reasoner")
    builders.add_conditional_edges("reasoner", tools_condition)
    builders.add_edge("tools", "reasoner")

    # Compile and visualize the graph
    react_graphs = builders.compile()
    # display(Image(react_graphs.get_graph(xray=True).draw_mermaid_png()))
    return react_graphs

# Call the function to build and display the graph
build_graph()

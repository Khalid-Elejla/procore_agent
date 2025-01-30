import os
from dotenv import load_dotenv

load_dotenv()

from .utils.helper_functions import get_langfuse_handler #, suppress_print
from .graphs.graph import build_graph

# Main execution
def run_agent_graph(query: str) -> str:

  # query = "give more information about Grashavyr Boogodyr"
  
  # Initialize Langfuse handler (assuming you are storing the keys in .env)
  langfuse_handler = get_langfuse_handler()

  # Build the state graph
  assistant_graph = build_graph()
  
  access_token = os.getenv('access_token')
  company_id = os.getenv('PROCORE_COMPANY_ID')

#================================================================================================
# Human in the loop
  from langgraph.types import Command
  # thread_config = {"configurable": {"thread_id": "1"}}

  # result = assistant_graph.invoke({"query": query, "messages": []}, config={"callbacks": [langfuse_handler],"thread_id": "1"},)
  # result = assistant_graph.invoke(Command(resume=True), config={"callbacks": [langfuse_handler],"thread_id": "1"},)
  result = assistant_graph.invoke({"query": query, "messages": []}, config={"callbacks": [langfuse_handler],"thread_id": "1"})

  import streamlit  as st
  while True:
    config = {"configurable": {"thread_id": "1"}}
    snapshot = assistant_graph.get_state(config)
    st.write(snapshot.next)
        
    if snapshot.next == ('human',):
      result = assistant_graph.invoke(Command(resume="I dont know assume any missing information, its for test purpose only"), config={"callbacks": [langfuse_handler],"thread_id": "1"},)
      break
    else:
      result = assistant_graph.invoke({"query": query, "messages": []}, config={"callbacks": [langfuse_handler],"thread_id": "1"})
# #================================================================================================

  # result = assistant_graph.invoke({"query": query, "messages": []}, config={"callbacks": [langfuse_handler]})

  # with suppress_print():      
  #     result = assistant_graph.invoke({"query": query, "messages": []}, config={"callbacks": [langfuse_handler]})

  # # Display the result
  # result['messages'][-1].pretty_print()
  return result['messages'][-1]



if __name__ == "__main__":
    run_agent_graph()

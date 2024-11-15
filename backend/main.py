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

  result = assistant_graph.invoke({"query": query, "messages": []}, config={"callbacks": [langfuse_handler]})

  # with suppress_print():      
  #     result = assistant_graph.invoke({"query": query, "messages": []}, config={"callbacks": [langfuse_handler]})

  # # Display the result
  # result['messages'][-1].pretty_print()

  return result['messages'][-1]



if __name__ == "__main__":
    run_agent_graph()
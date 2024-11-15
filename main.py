# import os
# from backend.main import run_agent_graph
# import streamlit as st
# from app.utils.auth import authenticate
# from dotenv import load_dotenv

# def main():
#     st.set_page_config(page_title="Procore AI Assistant", layout="wide")
    
#     # Sidebar section for file management
#     st.sidebar.subheader("File Upload")
#     uploaded_file = st.sidebar.file_uploader("Upload your document", type=["pdf", "docx", "txt", "xls"])

#     # # Ensure `uploaded_files` is initialized in session state
#     if "uploaded_files" not in st.session_state:
#         st.session_state.uploaded_files = []

#     # Add newly uploaded file to the list
#     if uploaded_file is not None:
#         st.session_state.uploaded_files.append(uploaded_file)
#         st.sidebar.success(f"{uploaded_file.name} uploaded successfully")


#     # Initialize chat session state
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Run authentication check
#     access_token = authenticate()

#     # Proceed only if authenticated
#     if access_token:
#         # Input for user message
#         user_input = st.chat_input("Type your question here...")

#         # Re-authenticate if token has expired before handling the user input
#         access_token = authenticate()  # This will re-check the token
#         # Set the access token as an environment variable
#         os.environ['access_token'] = access_token

#         if user_input and access_token:  # Only proceed if still authenticated
#             # Get a response from the agent
#             response = run_agent_graph(query=user_input)
#             st.session_state.messages.append({"user": user_input, "assistant": response.content})

#         # Display previous chat history
#         if st.session_state.messages:
#             st.markdown(
#                 "<h2 style='color: #800080;'>PROCORE AI Assistant</h2>",
#                 unsafe_allow_html=True
#             )
#             for message in st.session_state.messages:
#                 st.chat_message("user").write(message['user'])
#                 st.chat_message("assistant").write(message['assistant'])

# if __name__ == "__main__":
#     main()
# main.py
#===================================================================================================================
# # main.py
# import os
# import streamlit as st
# from datetime import datetime
# from backend.main import run_agent_graph
# from app.utils.auth import authenticate  # Ensure correct import based on your directory structure

# def main():
#   st.set_page_config(page_title="Procore AI Assistant", layout="wide")

#   # Run authentication check
#   access_token = authenticate()

#   # Proceed only if authenticated
#   if access_token:
#       # Sidebar section for file management
#       st.sidebar.subheader("File Upload")
#       uploaded_file = st.sidebar.file_uploader("Upload your document", type=["pdf", "docx", "txt", "xls"])

#       # Ensure 'uploaded_files' is initialized in session state
#       if "uploaded_files" not in st.session_state:
#           st.session_state.uploaded_files = []

#       # Add newly uploaded file to the list
#       if uploaded_file is not None:
#           st.session_state.uploaded_files.append(uploaded_file)
#           st.sidebar.success(f"{uploaded_file.name} uploaded successfully")

#       # Initialize chat session state
#       if "messages" not in st.session_state:
#           st.session_state.messages = []

#       # Input for user message
#       user_input = st.chat_input("Type your question here...")

#       # Set the access token as an environment variable
#       os.environ['access_token'] = access_token

#       if user_input:
#           # Get a response from the agent
#           response = run_agent_graph(query=user_input)
#           st.session_state.messages.append({"user": user_input, "assistant": response.content})

#       # Display previous chat history
#       if st.session_state.messages:
#           st.markdown(
#               "<h2 style='color: #800080;'>PROCORE AI Assistant</h2>",
#               unsafe_allow_html=True
#           )
#           for message in st.session_state.messages:
#               st.chat_message("user").write(message['user'])
#               st.chat_message("assistant").write(message['assistant'])
#   else:
#       st.warning("Please authenticate to continue.")
#       st.stop()

# if __name__ == "__main__":
#   main()
#============================================================
# import os
# import streamlit as st
# from datetime import datetime
# from backend.main import run_agent_graph
# from app.utils.auth import authenticate  # Ensure correct import based on your directory structure

# def main():
#     st.set_page_config(page_title="Procore AI Assistant", layout="wide")

#     # Add a custom title and a description
#     st.title("Welcome to Procore AI Assistant")
#     st.markdown("### How can I assist you today?")

#     # Run authentication check
#     access_token = authenticate()

#     # Proceed only if authenticated
#     if access_token:
#         # Sidebar section for file management with an attractive header
#         with st.sidebar:
#             st.subheader("📂 File Upload")
#             uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt", "xls"])

#             # Ensure 'uploaded_files' is initialized in session state
#             if "uploaded_files" not in st.session_state:
#                 st.session_state.uploaded_files = []

#             # Add newly uploaded file to the list
#             if uploaded_file is not None:
#                 st.session_state.uploaded_files.append(uploaded_file)
#                 st.success(f"{uploaded_file.name} uploaded successfully!")

#         # Initialize chat session state
#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         # Chat input for user messages
#         user_input = st.chat_input("Type your question here...")

#         # Set the access token as an environment variable
#         os.environ['access_token'] = access_token

#         # When the user submits a query
#         # if user_input:
#         #     with st.spinner("Thinking..."):
#         #         response = run_agent_graph(query=user_input)
#         #     st.session_state.messages.append({"user": user_input, "assistant": response.content})
#         if user_input:
#             # Display previous chat history
#             if st.session_state.messages:
#                 st.markdown(
#                     "<h2 style='color: #800080;'>PROCORE AI Assistant</h2>",
#                     unsafe_allow_html=True
#                 )
#                 for message in st.session_state.messages:
#                     st.chat_message("user").write(message['user'])
#                     st.chat_message("assistant").write(message['assistant'])

#             # Show thinking spinner below previous messages
#             with st.spinner("Thinking..."):
#                 # Get a response from the agent
#                 response = run_agent_graph(query=user_input)
#                 st.session_state.messages.append({"user": user_input, "assistant": response.content})





#         # Display previous chat history with more interactive design
#         if st.session_state.messages:
#             for message in st.session_state.messages:
#                 st.chat_message("user").markdown(f"**You:** {message['user']}")
#                 st.chat_message("assistant").markdown(f"**Assistant:** {message['assistant']}")

#     else:
#         st.warning("Please authenticate to continue.")
#         st.stop()

# if __name__ == "__main__":
#     main()
#===================================================
# import os
# import streamlit as st
# from datetime import datetime
# from backend.main import run_agent_graph
# from app.utils.auth import authenticate, clear_auth_state

# def initialize_session_state():
#   """Initialize session state variables"""
#   if "messages" not in st.session_state:
#       st.session_state.messages = []
#   if "uploaded_files" not in st.session_state:
#       st.session_state.uploaded_files = []

# def main():
#   st.set_page_config(page_title="Procore AI Assistant", layout="wide")

#   # Initialize session state
#   initialize_session_state()

#   # Add a custom title and a description
#   st.title("Welcome to Procore AI Assistant")
#   st.markdown("### How can I assist you today?")

#   # Add a logout button in the sidebar
#   with st.sidebar:
#       if st.button("Logout"):
#           clear_auth_state()
#           st.rerun()

#   # Run authentication check
#   access_token = authenticate()

#   # Proceed only if authenticated
#   if access_token:
#       try:
#           # Sidebar section for file management
#           with st.sidebar:
#               st.subheader("📂 File Upload")
#               uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt", "xls"])

#               if uploaded_file is not None:
#                   st.session_state.uploaded_files.append(uploaded_file)
#                   st.success(f"{uploaded_file.name} uploaded successfully!")

#           # Chat input for user messages
#           user_input = st.chat_input("Type your question here...")

#           # Set the access token as an environment variable
#           os.environ['access_token'] = access_token

#           if user_input:
#               # Display previous chat history
#               if st.session_state.messages:
#                   st.markdown(
#                       "<h2 style='color: #800080;'>PROCORE AI Assistant</h2>",
#                       unsafe_allow_html=True
#                   )
#                   for message in st.session_state.messages:
#                       st.chat_message("user").write(message['user'])
#                       st.chat_message("assistant").write(message['assistant'])

#               # Show thinking spinner below previous messages
#               with st.spinner("Thinking..."):
#                   response = run_agent_graph(query=user_input)
#                   st.session_state.messages.append({
#                       "user": user_input,
#                       "assistant": response.content
#                   })

#           # Display chat history
#           if st.session_state.messages:
#               for message in st.session_state.messages:
#                   st.chat_message("user").markdown(f"**You:** {message['user']}")
#                   st.chat_message("assistant").markdown(f"**Assistant:** {message['assistant']}")

#       except Exception as e:
#           st.error(f"An error occurred: {str(e)}")
#           clear_auth_state()
#           st.rerun()

#   else:
#       st.warning("Please authenticate to continue.")
#       st.stop()

# if __name__ == "__main__":
#   main()

#===================
# import os
# import streamlit as st
# from datetime import datetime
# from backend.main import run_agent_graph
# from app.utils.auth import authenticate, clear_auth_state

# def initialize_session_state():
#     """Initialize session state variables"""
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
#     if "uploaded_files" not in st.session_state:
#         st.session_state.uploaded_files = []

# def main():
#     st.set_page_config(page_title="Procore AI Assistant", layout="wide")

#     # Initialize session state
#     initialize_session_state()

#     # Add a custom title and a description
#     st.title("Welcome to Procore AI Assistant")
#     st.markdown("### How can I assist you today?")

#     # Check authentication state
#     access_token = authenticate()

#     # Sidebar section for login/logout
#     with st.sidebar:
#         if access_token:
#             if st.button("Logout"):
#                 clear_auth_state()
#                 st.success("You have been logged out.")
#                 st.experimental_rerun()  # Refresh the page to update the UI
#         else:
#             if st.button("Login"):
#                 st.markdown(f"[Click here to authorize the application]({os.getenv('AUTHORIZATION_URL')}?client_id={os.getenv('PROCORE_CLIENT_ID')}&response_type=code&redirect_uri={os.getenv('REDIRECT_URI')})", unsafe_allow_html=True)
#                 st.stop()

#     # Proceed only if authenticated
#     if access_token:
#         try:
#             # Sidebar section for file management
#             with st.sidebar:
#                 st.subheader("📂 File Upload")
#                 uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt", "xls"])

#                 if uploaded_file is not None:
#                     st.session_state.uploaded_files.append(uploaded_file)
#                     st.success(f"{uploaded_file.name} uploaded successfully!")

#             # Chat input for user messages
#             user_input = st.chat_input("Type your question here...")

#             # Set the access token as an environment variable
#             os.environ['access_token'] = access_token

#             if user_input:
#                 # Display previous chat history
#                 if st.session_state.messages:
#                     st.markdown(
#                         "<h2 style='color: #800080;'>PROCORE AI Assistant</h2>",
#                         unsafe_allow_html=True
#                     )
#                     for message in st.session_state.messages:
#                         st.chat_message("user").write(message['user'])
#                         st.chat_message("assistant").write(message['assistant'])

#                 # Show thinking spinner below previous messages
#                 with st.spinner("Thinking..."):
#                     response = run_agent_graph(query=user_input)
#                     st.session_state.messages.append({
#                         "user": user_input,
#                         "assistant": response.content
#                     })

#             # Display chat history
#             if st.session_state.messages:
#                 for message in st.session_state.messages:
#                     st.chat_message("user").markdown(f"**You:** {message['user']}")
#                     st.chat_message("assistant").markdown(f"**Assistant:** {message['assistant']}")

#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
#             clear_auth_state()
#             st.experimental_rerun()  # Refresh the page to update the UI

#     else:
#         st.warning("Please authenticate to continue.")
#         st.stop()

# if __name__ == "__main__":
#     main()

import os
import streamlit as st
from datetime import datetime
from backend.main import run_agent_graph
from app.utils.auth import authenticate, clear_auth_state

def initialize_session_state():
  """Initialize session state variables"""
  if "messages" not in st.session_state:
      st.session_state.messages = []
  if "uploaded_files" not in st.session_state:
      st.session_state.uploaded_files = []

def main():
  st.set_page_config(page_title="Procore AI Assistant", layout="wide")

  # Initialize session state
  initialize_session_state()

  # Add a custom title and a description
  st.title("Welcome to Procore AI Assistant")
  st.markdown("### How can I assist you today?")

  # Add a logout button in the sidebar
  with st.sidebar:
      if st.button("Logout"):
          clear_auth_state()
          st.rerun()

  # Run authentication check
  access_token = authenticate()

  # Proceed only if authenticated
  if access_token:
      try:
          # Sidebar section for file management
          with st.sidebar:
              st.subheader("📂 File Upload")
              uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt", "xls"])

              if uploaded_file is not None:
                  st.session_state.uploaded_files.append(uploaded_file)
                  st.success(f"{uploaded_file.name} uploaded successfully!")

          # Chat input for user messages
          user_input = st.chat_input("Type your question here...")

          # Set the access token as an environment variable
          os.environ['access_token'] = access_token

          if user_input:
              # Display previous chat history
              if st.session_state.messages:
                  st.markdown(
                      "<h2 style='color: #800080;'>PROCORE AI Assistant</h2>",
                      unsafe_allow_html=True
                  )
                  for message in st.session_state.messages:
                      st.chat_message("user").write(message['user'])
                      st.chat_message("assistant").write(message['assistant'])

              # Show thinking spinner below previous messages
              with st.spinner("Thinking..."):
                  response = run_agent_graph(query=user_input)
                  st.session_state.messages.append({
                      "user": user_input,
                      "assistant": response.content
                  })

          # Display chat history
          if st.session_state.messages:
              for message in st.session_state.messages:
                  st.chat_message("user").markdown(f"**You:** {message['user']}")
                  st.chat_message("assistant").markdown(f"**Assistant:** {message['assistant']}")

      except Exception as e:
          st.error(f"An error occurred: {str(e)}")
          clear_auth_state()
          st.rerun()

  else:
      st.warning("Please authenticate to continue.")
      st.stop()

if __name__ == "__main__":
  main()
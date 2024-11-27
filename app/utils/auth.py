# import os
# import requests
# import streamlit as st
# from datetime import datetime, timedelta

# # Procore credentials
# PROCORE_CLIENT_ID = os.getenv("PROCORE_CLIENT_ID")
# PROCORE_CLIENT_SECRET = os.getenv("PROCORE_CLIENT_SECRET")
# REDIRECT_URI= os.getenv("REDIRECT_URI")
# AUTHORIZATION_URL= os.getenv("AUTHORIZATION_URL") 
# TOKEN_URL= os.getenv("TOKEN_URL")


# def authenticate():
#     # Check if we already have a valid token in session_state
#     if "access_token" in st.session_state and st.session_state["token_expires_at"] > datetime.now():
#         return st.session_state["access_token"]

#     # Step 1: Prompt user for authorization if not authenticated
#     auth_url = f"{AUTHORIZATION_URL}?client_id={PROCORE_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"

#     st.write(f"[Click here to authorize the application]({auth_url})")

#     # Step 2: Capture the authorization code (in real case, use a callback to handle redirection)
#     code = st.text_input("Enter the authorization code:")

#     # Step 3: Exchange code for access token
#     if code:
#         token_data = {
#             'grant_type': 'authorization_code',
#             'code': code,
#             'client_id': PROCORE_CLIENT_ID,
#             'client_secret': PROCORE_CLIENT_SECRET,
#             'redirect_uri': REDIRECT_URI
#         }
#         response = requests.post(TOKEN_URL, data=token_data)

#         if response.status_code == 200:
#             token_info = response.json()
#             st.session_state["access_token"] = token_info["access_token"]
#             st.session_state["token_expires_at"] = datetime.now() + timedelta(seconds=token_info["expires_in"])
#             st.success("Authenticated successfully!")
#             return st.session_state["access_token"]
#         else:
#             st.error("Authentication failed. Please try again.")
#     return None

# auth.py
# auth.py
# import os
# import requests
# import streamlit as st
# from datetime import datetime, timedelta

# # Procore credentials
# PROCORE_CLIENT_ID = os.getenv("PROCORE_CLIENT_ID")
# PROCORE_CLIENT_SECRET = os.getenv("PROCORE_CLIENT_SECRET")
# REDIRECT_URI = os.getenv("REDIRECT_URI")
# AUTHORIZATION_URL = os.getenv("AUTHORIZATION_URL")
# TOKEN_URL = os.getenv("TOKEN_URL")

# def authenticate():
#   # Check if we already have a valid token in session_state
#   if (
#       "access_token" in st.session_state
#       and st.session_state["token_expires_at"] > datetime.now()
#   ):
#       return st.session_state["access_token"]

#   # Create the authorization URL
#   auth_url = f"{AUTHORIZATION_URL}?client_id={PROCORE_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"

#   # Check if code is in query params
#   query_params = st.get_query_params
#   code = query_params.get('code', [None])[0]

#   if code:
#       # Exchange code for access token
#       token_data = {
#           'grant_type': 'authorization_code',
#           'code': code,
#           'client_id': PROCORE_CLIENT_ID,
#           'client_secret': PROCORE_CLIENT_SECRET,
#           'redirect_uri': REDIRECT_URI
#       }

#       # Add debug information
#       st.write("Attempting to exchange code for access token...")
#       st.write("Token request data:")
#       st.write(token_data)

#       response = requests.post(TOKEN_URL, data=token_data)

#       if response.status_code == 200:
#           token_info = response.json()
#           st.session_state["access_token"] = token_info["access_token"]
#           st.session_state["token_expires_at"] = datetime.now() + timedelta(seconds=token_info["expires_in"])
#           st.success("Authenticated successfully!")
#           # Clear the query parameters from the URL
#           st.query_params
#           return st.session_state["access_token"]
#       else:
#           st.error("Authentication failed. Please try again.")
#           st.write(f"Error details: {response.status_code} - {response.text}")
#           # Optionally, clear the query parameters
#           st.query_params
#   else:
#       # Prompt user to click the link to authorize
#       st.write(f"[Click here to authorize the application]({auth_url})")
#       st.stop()  # Stop further execution until authentication is complete

#   return None
#=====================================================================================
# import os
# import requests
# import streamlit as st
# from datetime import datetime, timedelta

# # Procore credentials
# PROCORE_CLIENT_ID = os.getenv("PROCORE_CLIENT_ID")
# PROCORE_CLIENT_SECRET = os.getenv("PROCORE_CLIENT_SECRET")
# REDIRECT_URI = os.getenv("REDIRECT_URI")
# AUTHORIZATION_URL = os.getenv("AUTHORIZATION_URL")
# TOKEN_URL = os.getenv("TOKEN_URL")

# # def authenticate():
# #     # Check if we already have a valid token in session_state
# #     if (
# #         "access_token" in st.session_state
# #         and st.session_state["token_expires_at"] > datetime.now()
# #     ):
# #         return st.session_state["access_token"]

# #     # Create the authorization URL
# #     auth_url = f"{AUTHORIZATION_URL}?client_id={PROCORE_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"

# #     # Check if code is in query params
# #     query_params = st.query_params  # Correct method to retrieve query params
# #     code = query_params.get('code', [None])[0]

# #     if code:
# #         # Exchange code for access token
# #         token_data = {
# #             'grant_type': 'authorization_code',
# #             'code': code,
# #             'client_id': PROCORE_CLIENT_ID,
# #             'client_secret': PROCORE_CLIENT_SECRET,
# #             'redirect_uri': REDIRECT_URI
# #         }

# #         st.spinner("Attempting to authenticate...")  # Show spinner while authenticating
# #         response = requests.post(TOKEN_URL, data=token_data)

# #         if response.status_code == 200:
# #             token_info = response.json()
# #             st.session_state["access_token"] = token_info["access_token"]
# #             st.session_state["token_expires_at"] = datetime.now() + timedelta(seconds=token_info["expires_in"])
# #             st.success("Authentication successful! 🎉")
# #             st.rerun()  # Refresh the page to clear query params and proceed
# #             return st.session_state["access_token"]
# #         else:
# #             st.error("Authentication failed. Please try again.")
# #             st.write(f"Error details: {response.status_code} - {response.text}")
# #     else:
# #         # Prompt user to click the link to authorize
# #         st.markdown(f"[Click here to authorize the application]({auth_url})", unsafe_allow_html=True)
# #         st.stop()  # Stop further execution until authentication is complete

# #     return None
# def authenticate():
#   # Check if we already have a valid token in session_state
#   if (
#       "access_token" in st.session_state
#       and "token_expires_at" in st.session_state
#       and st.session_state["token_expires_at"] > datetime.now()
#   ):
#       return st.session_state["access_token"]

#   # Create the authorization URL
#   auth_url = f"{AUTHORIZATION_URL}?client_id={PROCORE_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"

#   # Check if code is in query params
#   query_params = st.query_params
#   code = query_params.get('code', [None])[0]

#   if code:
#       # Exchange code for access token
#       token_data = {
#           'grant_type': 'authorization_code',
#           'code': code,
#           'client_id': PROCORE_CLIENT_ID,
#           'client_secret': PROCORE_CLIENT_SECRET,
#           'redirect_uri': REDIRECT_URI
#       }

#       try:
#           response = requests.post(
#               TOKEN_URL, 
#               data=token_data,
#               headers={'Content-Type': 'application/x-www-form-urlencoded'}
#           )
          
#           if response.status_code == 200:
#               token_info = response.json()
#               st.session_state["access_token"] = token_info["access_token"]
#               st.session_state["token_expires_at"] = datetime.now() + timedelta(seconds=token_info["expires_in"])
#               # Clear the code from URL
#               st.query_params
#               return st.session_state["access_token"]
#           else:
#               st.error(f"Authentication failed: {response.status_code}")
#               st.json(response.json())
#               # Clear the code from URL as it's no longer valid
#               st.query_params
#               return None
              
#       except Exception as e:
#           st.error(f"Authentication error: {str(e)}")
#           return None
#   else:
#       st.markdown(f"[Click here to authorize the application]({auth_url})", unsafe_allow_html=True)
#       st.stop()

#   return None
#==================================================================================

import os
import requests
import streamlit as st
from datetime import datetime, timedelta
import logging

# Procore credentials
PROCORE_CLIENT_ID = os.getenv("PROCORE_CLIENT_ID")
PROCORE_CLIENT_SECRET = os.getenv("PROCORE_CLIENT_SECRET")

uris = [
      os.getenv("LOCAL_REDIRECT_URI"),
      os.getenv("PRODUCTION_REDIRECT_URI")
  ]


# Get the current URL using Streamlit's experimental get_query_params
def get_current_url():
    
  try:
      current_url = st.query_params.get('_stcore_url_', [''])[0]
      logging.error("yesooooooo",current_url)

  except:
      current_url = ''
      logging.error("Noooooooo",current_url)

      
  return current_url

# current_url = get_current_url()
current_url = os.getenv("PRODUCTION_REDIRECT_URI")

#current_url = st.get_option("server.baseUrlPath")


if "streamlit.app" in current_url:
    logging.error("yes",current_url)
    REDIRECT_URI = uris[1]  # Return production URI
else:
    logging.error("no",current_url)
    REDIRECT_URI = uris[0]

# REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTHORIZATION_URL = os.getenv("AUTHORIZATION_URL")
TOKEN_URL = os.getenv("TOKEN_URL")

def clear_auth_state():
  """Clear all authentication related session state"""
  if 'access_token' in st.session_state:
      del st.session_state['access_token']
  if 'refresh_token' in st.session_state:
      del st.session_state['refresh_token']
  if 'token_expires_at' in st.session_state:
      del st.session_state['token_expires_at']
  # Clear query parameters
  st.query_params.clear()

def refresh_token():
  """Attempt to refresh the access token"""
  if 'refresh_token' not in st.session_state:
      return False

  refresh_data = {
      'grant_type': 'refresh_token',
      'refresh_token': st.session_state['refresh_token'],
      'client_id': PROCORE_CLIENT_ID,
      'client_secret': PROCORE_CLIENT_SECRET
  }

  try:
      response = requests.post(
          TOKEN_URL,
          data=refresh_data,
          headers={'Content-Type': 'application/x-www-form-urlencoded'}
      )

      if response.status_code == 200:
          token_info = response.json()
          st.session_state["access_token"] = token_info["access_token"]
          st.session_state["refresh_token"] = token_info.get("refresh_token", st.session_state["refresh_token"])
          st.session_state["token_expires_at"] = datetime.now() + timedelta(seconds=token_info["expires_in"])
          return True
      else:
          clear_auth_state()
          return False

  except Exception as e:
      st.error(f"Token refresh error: {str(e)}")
      clear_auth_state()
      return False

def authenticate():
  """Main authentication function"""
  # Check if we have a valid token
  if (
      "access_token" in st.session_state
      and "token_expires_at" in st.session_state
  ):
      # If token is about to expire in the next 5 minutes, try to refresh it
      if datetime.now() + timedelta(minutes=5) >= st.session_state["token_expires_at"]:
          if refresh_token():
              return st.session_state["access_token"]
      # If token is still valid, use it
      elif st.session_state["token_expires_at"] > datetime.now():
          return st.session_state["access_token"]

  # Create the authorization URL
  auth_url = f"{AUTHORIZATION_URL}?client_id={PROCORE_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"

  # Check if code is in query params
  query_params = st.query_params
  code = query_params.get('code')

  if code:
      # Exchange code for access token
      token_data = {
          'grant_type': 'authorization_code',
          'code': code,
          'client_id': PROCORE_CLIENT_ID,
          'client_secret': PROCORE_CLIENT_SECRET,
          'redirect_uri': REDIRECT_URI
      }

      try:
          with st.spinner("Authenticating..."):
              response = requests.post(
                  TOKEN_URL, 
                  data=token_data,
                  headers={'Content-Type': 'application/x-www-form-urlencoded'}
              )
              
              if response.status_code == 200:
                  token_info = response.json()
                  st.session_state["access_token"] = token_info["access_token"]
                  st.session_state["refresh_token"] = token_info.get("refresh_token")
                  st.session_state["token_expires_at"] = datetime.now() + timedelta(seconds=token_info["expires_in"])
                  # Clear the code from URL
                  st.query_params.clear()
                  st.success("Successfully authenticated!")
                  st.rerun()
                  return st.session_state["access_token"]
              else:
                  st.error(f"Authentication failed: {response.status_code}")
                  st.json(response.json())
                  clear_auth_state()
                  return None
                  
      except Exception as e:
          st.error(f"Authentication error: {str(e)}")
          clear_auth_state()
          return None
  else:
      st.warning("Please authenticate to continue.")
      st.markdown(f"[Click here to authorize the application]({auth_url})", unsafe_allow_html=True)
      st.stop()

  return None
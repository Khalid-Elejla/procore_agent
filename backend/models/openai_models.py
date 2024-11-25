# openai_models.py

import os
from langchain_openai import ChatOpenAI

# Load API keys (environment variables can be set before running the app)
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

# Function to initialize the OpenAI LLM with API key
def load_openai_model():
    if OPENAI_API_KEY:
        return ChatOpenAI(temperature=0.1)
    else:
        raise ValueError("OpenAI API key not set. Please set OPENAI_API_KEY as an environment variable.")
from langfuse.callback import CallbackHandler
import sys
import os
import contextlib
from io import StringIO

# Define the langfuse handler (using environment variables for secret keys)
def get_langfuse_handler() -> CallbackHandler:
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    host = os.getenv("LANGFUSE_HOST")
    return CallbackHandler(secret_key=secret_key, public_key=public_key, host=host)

# Define a context manager to suppress print statements
@contextlib.contextmanager
def suppress_print():
  # Save the current standard output
  original_stdout = sys.stdout
  # Redirect standard output to a null device
  sys.stdout = StringIO()
  try:
      yield
  finally:
      # Restore the original standard output
      sys.stdout = original_stdout
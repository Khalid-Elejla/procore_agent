import logging
from ..models.openai_models import load_openai_model 
from langchain_community.utilities import SQLDatabase
from .dataframe_manager import DataFrameManager
from .database_toolkit import CustomSQLDatabaseToolkit


def initialize_db_tools(
    db_uri: str,  # Default database URI
    model_name: str = "gpt-4o-mini",  # Default model name
    temperature: float = 0.0,  # Default temperature for the model
    df_manager: DataFrameManager = None,  # Optional, default to None if no custom manager is provided
):
    """
    Initializes the SQL database toolkit and retrieves tools for interaction.
    This function sets up the OpenAI model, dataframe manager, and connects
    to the SQL database before fetching the tools needed for operations.
    
    Args:
        model_name (str): The name of the OpenAI model to load.
        temperature (float): The temperature setting for the OpenAI model.
        db_uri (str): URI for connecting to the SQL database.
        df_manager (DataFrameManager): Optional custom dataframe manager; if None, a default will be used.
    
    Returns:
        list: A list of database tools from the custom toolkit, or None if an error occurs.
    """
    try:
        # Initialize the LLM (Language Learning Model) with the specified model name
        llm = load_openai_model(model=model_name, temperature=temperature)

        # Use provided DataFrame Manager or initialize a default one
        df_manager = df_manager if df_manager else DataFrameManager()

        # Initialize the SQL database connection using the provided URI
        db = SQLDatabase.from_uri(db_uri)

        # Set up the custom toolkit with the SQL database, LLM, and DataFrame manager
        toolkit = CustomSQLDatabaseToolkit(
            db=db, 
            llm=llm,
            tools_kwargs={"df_manager": df_manager}  # Pass DataFrame manager as a tool argument
        )
        logging.error(f"Error initializing tools: {toolkit}")
        # Fetch the tools from the custom toolkit
        sql_toolbox = toolkit.get_tools()

        # # Return the set of tools that can be used for database operations
        # logging.debug("Tools successfully initialized.")
        
        return sql_toolbox

    except Exception as e:
        logging.error(f"Error initializing tools: {e}")
        return None

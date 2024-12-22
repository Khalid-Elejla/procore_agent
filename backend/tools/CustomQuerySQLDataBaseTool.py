from langchain.tools import BaseTool
from langchain_core.tools import Tool
from typing import Any, Optional, Dict
from langchain.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
import pandas as pd

from typing import List, Tuple, Union


# Function to convert query result (str) into a pandas DataFrame
def convert_to_dataframe(query_result: str) -> Union[pd.DataFrame, str]:
    """
    Converts query result (string representation of a list of tuples) into a pandas DataFrame.
    
    Args:
        query_result (str): The result of the SQL query as a string.
    
    Returns:
        pd.DataFrame: A DataFrame representing the query result, or a string error message.
    """
    try:
        # Parse the string representation of a list of tuples into actual Python data structure
        query_result = eval(query_result)
        
        # Convert result to DataFrame
        df = pd.DataFrame(query_result)
        return df
    except Exception as e:
        return str(e)  # Return error message if conversion fails
    

def run_query(self, query):
    cursor = self.db.cursor()

    # Execute the query
    cursor.execute(query)

    # Fetch column names (headers)
    columns = [desc[0] for desc in cursor.description]  # Extracts column names from the cursor description

    # Fetch data
    data = cursor.fetchall()

    # Return both columns and data
    return columns, data


# Function to extract the schema (column names) and preview the first 3 records
def extract_schema_and_preview(df: pd.DataFrame) -> Tuple[List[str], pd.DataFrame]:
    """
    Extracts the schema (column names) of the DataFrame and previews the first 3 records.
    
    Args:
        df (pd.DataFrame): The DataFrame whose schema and preview are to be extracted.
    
    Returns:
        Tuple[List[str], pd.DataFrame]: A tuple containing the schema (column names) and the preview (first 3 records).
    """
    try:
        # Get column names (schema)
        schema = df.columns.tolist()
        
        # Preview the first 3 records
        preview = df.head(3)
        
        return schema, preview
    except Exception as e:
        return str(e), pd.DataFrame()  # Return error message if extraction fails



import pandas as pd
import uuid


#===========================================================================================
class CustomQuerySQLDataBaseTool2(QuerySQLDataBaseTool):
    response_format: str = "content_and_artifact"
    
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ):
        """Execute the SQL query and return results with DataFrame artifact."""


        result = self.db.run(query)

        cursor = self.db._execute(query, fetch="cursor")
        headers = list(cursor.keys())
        
        # Package headers with the result
        result_with_headers = {"headers": headers, "data": result}

        try:
            df = pd.DataFrame(eval(result))
            df.columns = headers    
        except Exception as e:
            df=pd.DataFrame()

        # # Create a summary of the DataFrame
        # summary = {
        #     "rows": len(df),
        #     "columns": list(df.columns),
        #     "preview": str(df.head(3)) if len(df) > 0 else "Empty DataFrame"
        # }


        # # content = f"Query executed successfully. Retrieved {len(df)} rows with columns: {', '.join(df.columns)}",
        # # artifact = {
        # #             "df_id": df_id,
        # #             "df_path": df_path,
        # #             "rows": len(df),
        # #             "columns": list(df.columns),
        # #             "preview": df.head(2).to_dict()  # Small preview for verification
        # #         }

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # if not isinstance(result, pd.DataFrame):
        #     # If result is a string (like an error message)
        #     if isinstance(result, str):
        #         return result,{"NANANAN"}
        #         # return {
        #         #     "result": result,
        #         #     "artifacts": {}
        #         # }
        #     # Try to convert result to DataFrame
        #     try:
        #         df = pd.DataFrame(result)
        #     except:
        #         df = pd.DataFrame([result])
        # else:
        #     df = result

        # Return both the string representation and DataFrame as artifact
        # return {
        #     "result": str(df),
        #     "artifacts": {"dataframe": df}
        # }
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        return result_with_headers, df.to_json()
#===========================================================================================

import pandas as pd
import uuid
from pydantic import Field

class DataFrameManager:
    def __init__(self):
        self.dataframes = {}  # Store DataFrames in memory

    def store_df(self, df: pd.DataFrame) -> str:
        """Store DataFrame in memory and return its ID."""
        df_id = str(uuid.uuid4())  # Generate a unique ID
        self.dataframes[df_id] = df
        return df_id

    def get_df(self, df_id: str) -> pd.DataFrame:
        """Retrieve DataFrame by ID."""
        return self.dataframes.get(df_id)

    def cleanup(self, df_id: str):
        """Remove DataFrame from memory."""
        if df_id in self.dataframes:
            del self.dataframes[df_id]


class CustomQuerySQLDataBaseTool(QuerySQLDataBaseTool):
    response_format: str = "content_and_artifact"
    df_manager: Any = Field(default=None, exclude=True)
    
    def __init__(self, db, df_manager, *args, **kwargs):
        super().__init__(db=db, *args, **kwargs)
        self.df_manager = df_manager  # Pass the DataFrameManager instance


    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ):
        """Execute the SQL query and return results with DataFrame artifact."""


        result = self.db.run(query)

        cursor = self.db._execute(query, fetch="cursor")
        headers = list(cursor.keys())
        
        # Package headers with the result
        result_with_headers = {"headers": headers, "data": result}

        try:
            df = pd.DataFrame(eval(result))
            df.columns = headers    
        except Exception as e:
            df=pd.DataFrame()

        # Store DataFrame in memory
        df_id = self.df_manager.store_df(df)

        content=f"Query executed successfully. Retrieved {len(df)} rows with columns: {', '.join(df.columns)}"
        artifact= {
                    "df_id": df_id,
                    "rows": len(df),
                    "columns": list(df.columns),
                    "preview": df.head(2).to_dict()  # Small preview for verification
        }
        return content, artifact

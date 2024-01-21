import pandas as pd
import json

def json_array_to_dataframe(json_array):
    try:
        # Parse the JSON string into Python objects (list of dictionaries)
        df = pd.DataFrame(json_array)

        # convert into json
        df = df.to_json(orient='records')
        return df


    except json.JSONDecodeError:
        # Handling invalid JSON format
        return "Invalid JSON format"
    except Exception as e:
        # Handling other exceptions
        return f"An error occurred: {e}"

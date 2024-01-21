import pandas as pd
import json

def json_array_to_dataframe(json_array):

    try:
        # Convert JSON array (string) to a Python list
        data_list = json.loads(json_array)

        # Normalize the JSON data and convert it to a DataFrame
        dataFrameJSON = pd.json_normalize(data_list)

        #Calculate the mean of the values in the column
        mean = dataFrameJSON['value'].mean()
        
        #add new column with mean value
        dataFrameJSON['mean'] = mean




        # Normalize the JSON data and convert it to a DataFrame
        return dataFrameJSON.to_json(orient="records")
    


    except Exception as e:
        print("Error converting JSON array to DataFrame:", e)
        return None

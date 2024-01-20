# import requests
# import pandas as pd

# def fetch_gios_data(indicator, page=0, size=20, sort='', wojewodztwo=''):
#     api_url = f'http://127.0.0.1:5000/api/gios-data?indicator={indicator}&page={page}&size={size}&sort={sort}&wojewodztwo={wojewodztwo}'
#     response = requests.get(api_url)
#     data = response.json()
    
#     # Convert the JSON data to a Pandas DataFrame
#     df = pd.DataFrame(data)
#     return df

# # Example usage
# df = fetch_gios_data('O3')
# print(df)
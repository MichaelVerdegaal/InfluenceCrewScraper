import requests
import time
import pandas as pd

crew_contract_address = '0x746db7b1728af413c4e2b98216c6171b2fc9d00e'
# We first need to a get a single adddress that owns a crew member to do the next query
single_asset_request_url = f"https://api.opensea.io/api/v1/asset/{crew_contract_address}/1/"
response = requests.request("GET", single_asset_request_url)
random_crew_owner = response.json()['owner']['address']

# Get minted crew count
collection_request_url = "https://api.opensea.io/api/v1/collections"
querystring = {"offset": "0", "limit": "300", "asset_owner": random_crew_owner}
response = requests.request("GET", collection_request_url, params=querystring)
crew_count = 0
for i in response.json():
    if i['primary_asset_contracts'][0]['name'] == "Influence Crew":
        crew_count = int(i['stats']['count'])
print(f"Retrieving {crew_count} total crew members")

# Collect crew members
crew_list = []
iteration_counter = 0
for i in range(int(crew_count / 50) + 1):
    time.sleep(1)
    print(f"Collecting crew {iteration_counter * 50}/{crew_count}")
    multi_asset_request_url = f"https://api.opensea.io/api/v1/assets"
    querystring = {"order_direction": "desc", "offset": f"{iteration_counter * 50}", "limit": "50",
                   "asset_contract_addresses": crew_contract_address}
    response = requests.request("GET", multi_asset_request_url, params=querystring)
    text = response.json()
    for crew in text['assets']:
        crew_list.append(crew)
    iteration_counter += 1

# Write to csv
print(f"Writing to csv")
df = pd.json_normalize(crew_list)
df.to_csv("crew.csv")

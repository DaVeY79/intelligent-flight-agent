import requests
import json

url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/UK/GBP/en-GB/"

querystring = {"query":"Stockholm"}
headers = {
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    'x-rapidapi-key': "5e95a68c99msh96592d58fcb9d95p17319bjsn5bcf6b61e6b5"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
json_data = json.loads(response.text)
depart_id = json_data["Places"][0]["PlaceId"]

querystring = {"query":"Oslo"}
response2 = requests.request("GET", url, headers=headers, params=querystring)
json_data2 = json.loads(response2.text)
arrival_id = json_data2["Places"][0]["PlaceId"]


new_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/IN/INR/en-IN/{}/{}/2020-04-01".format(depart_id,arrival_id)
new_querystring = {"inboundpartialdate":"2020-02-27"}
response3 = requests.request("GET", new_url, headers=headers, params=new_querystring)
json_data3 = json.loads(response3.text)
price = json_data3["Quotes"][0]["MinPrice"]
print(price)

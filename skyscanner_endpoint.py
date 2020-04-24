import requests
import json

headers = {
            'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
            'x-rapidapi-key': "5e95a68c99msh96592d58fcb9d95p17319bjsn5bcf6b61e6b5"
          }

url_template = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/{}/v1.0/{}/{}/{}/"

def get_place_id(place_name,booking_country="IN",currency="INR",locale="en-GB"):
    url = url_template.format("autosuggest",booking_country,currency,locale)
    response = requests.request("GET",
                                        url,
                                        headers=headers,
                                        params={"query":place_name})
    json_data = json.loads(response.text)
    place_id = json_data["Places"][0]["PlaceId"]
    return place_id


def get_routes(depart_id,arrival_id,departure_datetime,booking_country="IN",currency="INR",locale="en-GB"):
    url = url_template.format("browseroutes",booking_country,currency,locale) + "{}/{}/{}".format(depart_id,arrival_id,departure_datetime)
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    return json_data

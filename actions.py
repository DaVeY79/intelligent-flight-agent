# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import requests
import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionFlightSearch(Action):

    def name(self) -> Text:
        return "action_flight_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        flight_source = tracker.get_slot("fromloc.city_name")
        flight_destination = tracker.get_slot("toloc.city_name")

        url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/UK/GBP/en-GB/"
        headers = {
            'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
            'x-rapidapi-key': "5e95a68c99msh96592d58fcb9d95p17319bjsn5bcf6b61e6b5"
            }
        # new_querystring = {"inboundpartialdate":"2020-04-27"}

        response = requests.request("GET",
                                    url,
                                    headers=headers,
                                    params={"query":flight_source})
        json_data = json.loads(response.text)
        depart_id = json_data["Places"][0]["PlaceId"]

        response2 = requests.request("GET",
                                     url,
                                     headers=headers,
                                     params={"query":flight_destination})
        json_data2 = json.loads(response2.text)
        arrival_id = json_data2["Places"][0]["PlaceId"]

        new_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/IN/INR/en-IN/{}/{}/2020-09-01".format(depart_id,arrival_id)
        response3 = requests.request("GET", new_url, headers=headers)
        json_data3 = json.loads(response3.text)
        prices = json_data3["Quotes"]
        buttons = []

        if prices:
            for price in prices:
                carrier_id = price["OutboundLeg"]["CarrierIds"][0]
                carrier_name = list(filter(lambda x: x["CarrierId"] == carrier_id, json_data3["Carriers"]))[0]["Name"]
                buttons.append({"title":"Airline : {}, Price : ₹{}, Departure Time : {} ".format(carrier_name,price["MinPrice"],price["QuoteDateTime"][-8:]),"payload":"/quote{\"quote_id\":\""+str(price["QuoteId"])+"\"}"})
            dispatcher.utter_message(text="Checking about available flights for that route {} to {}. The following flights are available: ".format(flight_source,flight_destination),buttons=buttons)
        else:
            dispatcher.utter_message("No flights available for that route")
        return []

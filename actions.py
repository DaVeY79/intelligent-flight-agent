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
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction
from skyscanner_endpoint import get_place_id, get_routes

class ActionFlightSearch(Action):

    def name(self) -> Text:
        return "action_flight_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        flight_source = tracker.get_slot("fromloc.city_name")
        flight_destination = tracker.get_slot("toloc.city_name")
        departure_datetime = tracker.get_slot("time")

        depart_id = get_place_id(flight_source)
        arrival_id = get_place_id(flight_destination)
        json_data = get_routes(depart_id,arrival_id,str(departure_datetime)[:10])
        prices = json_data["Quotes"]
        buttons = []

        if prices:
            for price in prices:
                carrier_id = price["OutboundLeg"]["CarrierIds"][0]
                carrier_name = list(filter(lambda x: x["CarrierId"] == carrier_id, json_data["Carriers"]))[0]["Name"]
                buttons.append({"title":"Airline : {}, Price : ₹{}, Departure Time : {} ".format(carrier_name,price["MinPrice"],price["QuoteDateTime"][-8:]),"payload":"/quote{\"quote_id\":\""+str(price["QuoteId"])+"\"}"})
            dispatcher.utter_message(text="Checking about available flights for that route {} to {}. The following flights are available: ".format(flight_source,flight_destination),buttons=buttons)
        else:
            dispatcher.utter_message("No flights available for that route")
        return []

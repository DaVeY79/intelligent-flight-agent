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
from rasa_sdk.events import AllSlotsReset
# from skyscanner_endpoint import get_place_id, get_routes
from amadeus_endpoint import AmadeusFlight
from iata_mapping import get_city_name, get_airline_name
import re
import datetime


class ActionSlotReset(Action):

    def name(self) -> Text:
        return "action_slot_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [AllSlotsReset()]


class FlightBookingForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "flight_booking_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        if tracker.get_slot('child_passengers'):

            if tracker.get_slot('infant_passengers'):
                return ["fromloc.city_name", "toloc.city_name", "time", "no_of_adults", "child_passengers", "infant_passengers", "no_of_children", "no_of_infants", "class_type", "currency_code"]

            else:
                return ["fromloc.city_name", "toloc.city_name", "time", "no_of_adults", "child_passengers", "infant_passengers", "no_of_children", "class_type", "currency_code"]

        else:
            return ["fromloc.city_name", "toloc.city_name", "time", "no_of_adults", "child_passengers", "infant_passengers", "class_type", "currency_code"]


    def slot_mappings(self) -> Dict[Text, Any]:
        return {"fromloc.city_name": self.from_entity(entity="fromloc.city_name",
                                                      intent=["flight",
                                                              "inform_departure_city"]),

                "toloc.city_name": self.from_entity(entity="toloc.city_name",
                                                    intent=["flight",
                                                            "inform_arrival_city"]),

                "time": self.from_entity(entity="time",
                                                intent=["flight",
                                                        "inform_departure_date"]),

                "child_passengers": [self.from_intent(intent="affirm", value=True),
                                     self.from_intent(intent="deny", value=False)],

                "infant_passengers": [self.from_intent(intent="affirm", value=True),
                                      self.from_intent(intent="deny", value=False)],

                "no_of_adults": self.from_entity(entity="no_of_adults",
                                                 intent=["flight",
                                                         "inform_no_of_adults"]),

                "no_of_children": self.from_entity(entity="no_of_children",
                                                   intent=["flight",
                                                           "inform_no_of_children"]),

                "no_of_infants": self.from_entity(entity="no_of_infants",
                                                  intent=["flight",
                                                          "inform_no_of_infants"]),

                "class_type": self.from_entity(entity="class_type",
                                               intent=["flight","inform_class_type"]),

                "currency_code": self.from_entity(entity="currency_code",
                                                  intent=["flight","inform_currency_code"])}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""

        flight_source = tracker.get_slot("fromloc.city_name")
        flight_destination = tracker.get_slot("toloc.city_name")
        departure_datetime = tracker.get_slot("time")
        departure_datetime_ = re.split(r"[T,+,.]",str(departure_datetime))[:2]
        departure_date = departure_datetime_[0]
        departure_time = departure_datetime_[1]
        no_of_adults = int(tracker.get_slot("no_of_adults"))
        no_of_children = int(tracker.get_slot("no_of_children"))
        no_of_infants = int(tracker.get_slot("no_of_infants"))
        class_type = tracker.get_slot("class_type")
        currency_code = tracker.get_slot("currency_code")

        currency_code_mapping = {"USD":"US Dollars","EUR":"Euros","JPY":"Japanese Yen","GBP":"Pound Sterling","CHF":"Swiss Francs", "INR":"Indian Rupees","AUD":"Australian Dollars","CAD":"Canadian Dollars","CNY":"Chinese Yuan Renminbi"}


        adults = ""
        children = ""
        infants = ""

        if no_of_adults == 1:
            adults = "1 adult"
        elif no_of_adults > 1:
            adults = str(no_of_adults) + " adults"

        if no_of_children == 1:
            infants = "and 1 child"
        elif no_of_children > 1:
            infants = "and " + str(no_of_children) + " children"

        if no_of_infants == 1:
            infants = "and 1 infant"
        elif no_of_infants > 1:
            infants = "and " + str(no_of_infants) + " infants"

        out = "Checking information about available flights for the route {} --> {} on {} for {} {} {} in {} class. Payment currency is {}. The following flights are available: ".format(flight_source, flight_destination, str(departure_date)[:10], adults, children,
                                                                                                                                                                                      infants, class_type.title(), currency_code_mapping.get(currency_code))

        #dispatcher.utter_message(text=out)

        buttons = []

        try:
            a = AmadeusFlight(originLocation=flight_source, destinationLocation=flight_destination, departureDate=str(departure_date)[:10],adults=no_of_adults,children=no_of_children,infants=no_of_infants)
        except Exception:
            pass

        else:
            gfp = iter(a.generate_flight_prices())
            quote_id = 1

            while True:
                try:
                    output = next(gfp)
                    buttons.append({"title":output,"payload":"/quote{\"quote_id\":\""+str(quote_id)+"\"}"})
                    quote_id = quote_id + 1
                except StopIteration:
                    quote_id = 1
                    break

        if len(buttons) == 0:
            dispatcher.utter_message("No flights available for that route")
        else:
            dispatcher.utter_message(text=out,buttons=buttons)

        return []

    def validate_child_passengers(self,
                                  value: bool,
                                  dispatcher: CollectingDispatcher,
                                  tracker: Tracker,
                                  domain: Dict[Text, Any],
                                  ) -> Dict[Text, Any]:

        if value:
            return {"child_passengers": value}

        else:
            return [SlotSet("no_of_children", 0)]

    def validate_infant_passengers(self,
                                   value: bool,
                                   dispatcher: CollectingDispatcher,
                                   tracker: Tracker,
                                   domain: Dict[Text, Any],
                                   ) -> Dict[Text, Any]:

        if value:
            return {"infant_passengers": value}

        else:
            return [SlotSet("no_of_infants", 0)]


    def validate_no_of_children(self,
                                value: float,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: Dict[Text, Any],
                                ) -> Dict[Text, Any]:

        if value:
            return {"no_of_children": value}

        else:
            return [SlotSet("child_passengers", False)]

    def validate_no_of_infants(self,
                               value: float,
                               dispatcher: CollectingDispatcher,
                               tracker: Tracker,
                               domain: Dict[Text, Any],
                               ) -> Dict[Text, Any]:

        if value:
            return {"no_of_infants": value}

        else:
            return [SlotSet("infant_passengers", False)]

    # def validate_return_flight(self,
    #                                value: bool,
    #                                dispatcher: CollectingDispatcher,
    #                                tracker: Tracker,
    #                                domain: Dict[Text, Any],
    #                                ) -> Dict[Text, Any]:
    #     """Validate round trip or one way value."""
    #
    #     if value:
    #         return [FollowupAction(utter_ask_return_date),SlotSet("time", None)]
    #
    #     else:
    #         return {"return_flight": value}


    # def validate_return_date(self,
    #                   value: Text,
    #                   dispatcher: CollectingDispatcher,
    #                   tracker: Tracker,
    #                   domain: Dict[Text, Any],
    #                   ) -> Dict[Text, Any]:
    #     """Validate return date."""
    #
    #     time_val = re.split(r"[T,+,.]",str(tracker.get_slot('time')))[0]
    #     depart_date_val = datetime.datetime.strptime(str(tracker.get_slot('depart_date')),"%Y-%m-%d")
    #
    #     if tracker.get_slot('time') and time_val:
    #         return_date_val = datetime.datetime.strptime(time_val[0],"%Y-%m-%d")
    #         if return_date_val < depart_date_val:
    #             dispatcher.utter_message("Return date should be after the departure date")
    #             return [SlotSet(return_date,None),FollowupAction(utter_ask_return_date)]
    #         else:
    #             return [SlotSet("return_date",return_date_val),SlotSet("time",None)]
    #     else:
    #         return [SlotSet("return_date",None)]


    # def validate_time(self,
    #                   value: Text,
    #                   dispatcher: CollectingDispatcher,
    #                   tracker: Tracker,
    #                   domain: Dict[Text, Any],
    #                   ) -> Dict[Text, Any]:
    #     """Validate duckling time entity"""
    #
    #     if value:
    #         time_val = re.split(r"[T,+,.]",str(value))[:2]
    #         if tracker.get_slot('return_flight'):
    #             return_date_val = time_val[0]
    #             return [SlotSet("return_date",return_date_val),SlotSet("time",None)]
    #
    #         else:
    #             depart_date_val = time_val[0]
    #             return [SlotSet("depart_date", depart_date_val),SlotSet("time",None)]
    #
    #     else:
    #         return [SlotSet("time",None)]



    # def validate_depart_date(self,
    #                   value: Text,
    #                   dispatcher: CollectingDispatcher,
    #                   tracker: Tracker,
    #                   domain: Dict[Text, Any],
    #                   ) -> Dict[Text, Any]:
    #     """Validate departure date."""
    #
    #     if tracker.get_slot('time'):
    #         time_val = re.split(r"[T,+,.]",str(tracker.get_slot('time')))[:2]
    #         depart_date_val = time_val[0]
    #         return [SlotSet("depart_date",depart_date_val),SlotSet("time",None)]
    #
    #     else:
    #         return [SlotSet("depart_date", None)]

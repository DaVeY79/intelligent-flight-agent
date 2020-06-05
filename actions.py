# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import requests
import json
from typing import Any, Text, Dict, List, Optional, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, EventType
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset
from amadeus_endpoint import AmadeusFlight
from retrieve_information import RetrieveBookingInformation
from iata_mapping import get_city_name, get_city_iata, get_city_iatas, get_airline_name, get_airline_iata
import re
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
REQUESTED_SLOT = "requested_slot"

a = ""

class ActionSlotReset(Action):

    def name(self) -> Text:
        return "action_slot_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [AllSlotsReset()]


class ActionBookingConfirmation(Action):
    def name(self) -> Text:
        return "action_booking_confirmation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        quote_id = int(tracker.get_slot("quote_id"))
        global a
        try:
            pnr = a.insert_booking_details(quote_id-1)
        except:
            dispatcher.utter_message("Sorry booking unsuccessful. Please try again")
            return []
        else:
            dispatcher.utter_message("Booking successful. Your booking reference/pnr is {}".format(pnr))
            return []

class ActionAskFromAirport(Action):
    def name(self) -> Text:
        return "action_ask_from_airport"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city_name = tracker.get_slot("fromloc_city_name")
        if len(list(get_city_iatas(city_name))) > 1:
            buttons = []
            for city_airport_name,city,city_iata in get_city_iatas(city_name):
                buttons.append({"title":"I want a flight from {}, {}".format(city_airport_name,city_iata),"payload":"/inform_departure_airport_code{\"fromloc.airport_code\":\""+str(city_iata).lower()+"\"}"})

            out = "Please select the airport for {}: ".format(city_name)
            dispatcher.utter_message(text=out,buttons=buttons)
            return []

        else:
            flight_source = tracker.get_slot("fromloc_city_name")
            flight_source_iata = get_city_iata(flight_source)
            return [SlotSet("fromloc.airport_code",flight_source_iata)]



class ActionAskToAirport(Action):
    def name(self) -> Text:
        return "action_ask_to_airport"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city_name = tracker.get_slot("toloc_city_name")
        if len(list(get_city_iatas(city_name))) > 1:
            buttons = []
            for city_airport_name,city,city_iata in get_city_iatas(city_name):
                buttons.append({"title":"I want a flight to {}, {}".format(city_airport_name,city_iata),"payload":"/inform_arrival_airport_code{\"toloc.airport_code\":\""+str(city_iata).lower()+"\"}"})

            out = "Please select the airport for {}: ".format(city_name)

            dispatcher.utter_message(text=out,buttons=buttons)
            return []

        else:
            flight_destination = tracker.get_slot("toloc_city_name")
            flight_destination_iata = get_city_iata(flight_destination)
            return [SlotSet("toloc.airport_code",flight_destination_iata)]



class RetrieveBookingInfoForm(FormAction):
    def name(self) -> Text:
        return "retrieve_booking_info_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["pnr"]

    def slot_mappings(self) -> Dict[Text, Any]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""


        return {"pnr": self.from_entity(entity="pnr", intent=["inform_pnr"])}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any],
               ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        pnr = tracker.get_slot("pnr")
        r = RetrieveBookingInformation(pnr)
        out, title, user_name, email_id, country_code, mobile_no = r.get_booking_details()
        dispatcher.utter_message(out)

        return [SlotSet("title",title),SlotSet("user_name",user_name),SlotSet("email_id",email_id),SlotSet("country_code",country_code),SlotSet("mobile_no",mobile_no),SlotSet("pnr",None)]


class FlightBookingForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "flight_booking_form"


    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        if tracker.get_slot('child_passengers') and tracker.get_slot('infant_passengers') and tracker.get_slot("round_trip") == "round trip":

            return ["time","fromloc_city_name", "toloc_city_name", "depart_date", "no_of_adults", "child_passengers", "no_of_children", "infant_passengers", "no_of_infants", "class_type", "currency_code", "round_trip", "return_date", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]

        elif tracker.get_slot('child_passengers') and tracker.get_slot('infant_passengers') and not(tracker.get_slot("round_trip") == "round trip"):

            return ["time","fromloc_city_name", "toloc_city_name","depart_date", "no_of_adults", "child_passengers", "no_of_children", "infant_passengers", "no_of_infants", "class_type", "currency_code", "round_trip", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]

        elif tracker.get_slot('child_passengers') and not(tracker.get_slot('infant_passengers')) and tracker.get_slot("round_trip") == "round trip":

            return ["time","fromloc_city_name", "toloc_city_name", "depart_date", "no_of_adults", "child_passengers", "no_of_children", "infant_passengers", "class_type", "currency_code", "round_trip", "return_date", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]

        elif not(tracker.get_slot('child_passengers')) and tracker.get_slot('infant_passengers') and tracker.get_slot("round_trip") == "round trip":

            return ["time","fromloc_city_name", "toloc_city_name", "depart_date", "no_of_adults", "child_passengers", "infant_passengers", "no_of_infants", "class_type", "currency_code", "round_trip", "return_date", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]

        elif tracker.get_slot('child_passengers') and not(tracker.get_slot('infant_passengers')) and not(tracker.get_slot("round_trip") == "round trip"):

            return ["time","fromloc_city_name", "toloc_city_name", "depart_date", "no_of_adults", "child_passengers", "no_of_children", "infant_passengers", "class_type", "currency_code", "round_trip", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]

        elif not(tracker.get_slot('child_passengers')) and tracker.get_slot('infant_passengers') and not(tracker.get_slot("round_trip") == "round trip"):

            return ["time","fromloc_city_name", "toloc_city_name", "depart_date", "no_of_adults", "child_passengers", "infant_passengers", "no_of_infants", "class_type", "currency_code", "round_trip", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]

        elif not(tracker.get_slot('child_passengers')) and not(tracker.get_slot('infant_passengers')) and tracker.get_slot("round_trip") == "round trip":

            return ["time","fromloc_city_name", "toloc_city_name", "depart_date", "no_of_adults", "child_passengers", "infant_passengers", "class_type", "currency_code", "round_trip", "return_date", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]

        else:

            return ["time","fromloc_city_name", "toloc_city_name", "depart_date", "no_of_adults", "child_passengers", "infant_passengers", "class_type", "currency_code", "round_trip", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]


        # if tracker.get_slot('child_passengers') and tracker.get_slot('infant_passengers') and tracker.get_slot("round_trip") == "round trip":
        #
        #     return ["time","fromloc_city_name", "fromloc.airport_code", "toloc_city_name", "toloc.airport_code", "depart_date", "no_of_adults", "child_passengers", "no_of_children", "infant_passengers", "no_of_infants", "class_type", "currency_code", "round_trip", "return_date", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]
        #
        # elif tracker.get_slot('child_passengers') and tracker.get_slot('infant_passengers') and not(tracker.get_slot("round_trip") == "round trip"):
        #
        #     return ["time","fromloc_city_name", "fromloc.airport_code", "toloc_city_name", "toloc.airport_code", "depart_date", "no_of_adults", "child_passengers", "no_of_children", "infant_passengers", "no_of_infants", "class_type", "currency_code", "round_trip", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]
        #
        # elif tracker.get_slot('child_passengers') and not(tracker.get_slot('infant_passengers')) and tracker.get_slot("round_trip") == "round trip":
        #
        #     return ["time","fromloc_city_name", "fromloc.airport_code", "toloc_city_name",  "toloc.airport_code", "depart_date", "no_of_adults", "child_passengers", "no_of_children", "infant_passengers", "class_type", "currency_code", "round_trip", "return_date", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]
        #
        # elif not(tracker.get_slot('child_passengers')) and tracker.get_slot('infant_passengers') and tracker.get_slot("round_trip") == "round trip":
        #
        #     return ["time","fromloc_city_name", "fromloc.airport_code", "toloc_city_name", "toloc.airport_code", "depart_date", "no_of_adults", "child_passengers", "infant_passengers", "no_of_infants", "class_type", "currency_code", "round_trip", "return_date", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]
        #
        # elif tracker.get_slot('child_passengers') and not(tracker.get_slot('infant_passengers')) and not(tracker.get_slot("round_trip") == "round trip"):
        #
        #     return ["time","fromloc_city_name", "fromloc.airport_code", "toloc_city_name", "toloc.airport_code", "depart_date", "no_of_adults", "child_passengers", "no_of_children", "infant_passengers", "class_type", "currency_code", "round_trip", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]
        #
        # elif not(tracker.get_slot('child_passengers')) and tracker.get_slot('infant_passengers') and not(tracker.get_slot("round_trip") == "round trip"):
        #
        #     return ["time","fromloc_city_name", "fromloc.airport_code", "toloc_city_name", "toloc.airport_code", "depart_date", "no_of_adults", "child_passengers", "infant_passengers", "no_of_infants", "class_type", "currency_code", "round_trip", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]
        #
        # elif not(tracker.get_slot('child_passengers')) and not(tracker.get_slot('infant_passengers')) and tracker.get_slot("round_trip") == "round trip":
        #
        #     return ["time","fromloc_city_name", "fromloc.airport_code", "toloc_city_name", "toloc.airport_code", "depart_date", "no_of_adults", "child_passengers", "infant_passengers", "class_type", "currency_code", "round_trip", "return_date", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]
        #
        # else:
        #
        #     return ["time","fromloc_city_name", "fromloc.airport_code", "toloc_city_name", "toloc.airport_code", "depart_date", "no_of_adults", "child_passengers", "infant_passengers", "class_type", "currency_code", "round_trip", "flight_stop_check","email_id","title","user_name","mobile_no","country_code"]



    def slot_mappings(self) -> Dict[Text, Any]:
        return {"fromloc_city_name": self.from_entity(entity="fromloc_city_name",
                                                      intent=["flight",
                                                              "inform_departure_city"]),

                "toloc_city_name": self.from_entity(entity="toloc_city_name",
                                                    intent=["flight",
                                                            "inform_arrival_city"]),

                "fromloc.airport_code": [self.from_entity(entity="fromloc.airport_code",intent="inform_departure_airport_code"),
                                         self.from_text(intent="inform_departure_airport_code")],

                "toloc.airport_code": [self.from_entity(entity="fromloc.airport_code",intent="inform_arrival_airport_code"),
                                       self.from_text(intent="inform_arrival_airport_code")],

                "depart_date": self.from_entity(entity="time",
                                                intent=["flight",
                                                        "inform_departure_date"]),

                "time": self.from_entity(entity="time",
                                                intent=["flight",
                                                        "inform_departure_date", "inform_return_date"]),

                "child_passengers": [self.from_intent(intent="affirm", value=True),
                                     self.from_intent(intent="deny", value=False)],

                "infant_passengers": [self.from_intent(intent="affirm", value=True),
                                      self.from_intent(intent="deny", value=False)],

                "flight_stop_check": [self.from_intent(intent="affirm", value="true"),
                                      self.from_intent(intent="deny", value="false")],

                "no_of_adults": self.from_entity(entity="number",
                                                 intent=["inform_no_of_adults"]),

                "no_of_children": self.from_entity(entity="number",
                                                   intent=["inform_no_of_children"]),

                "no_of_infants": self.from_entity(entity="number",
                                                  intent=["inform_no_of_infants"]),

                "class_type": self.from_entity(entity="class_type",
                                               intent=["flight","inform_class_type"]),

                "currency_code": self.from_entity(entity="currency_code",
                                                  intent=["flight","inform_currency_code"]),

                "round_trip": self.from_entity(entity="round_trip",
                                                  intent=["flight","inform_round_trip"]),

                "return_date": self.from_entity(entity="time",
                                                  intent=["inform_return_date"]),

                "email_id": self.from_entity(entity="email_id",
                                                  intent=["inform_email_id"]),

                "title": self.from_text(intent=None),

                "user_name": self.from_entity(entity="user_name",
                                                  intent=["inform_user_name"]),

                "mobile_no": self.from_entity(entity="mobile_no",
                                                  intent=["inform_mobile_no"]),

                "country_code": [self.from_entity(entity="number",
                                                  intent=["inform_country_code"]),
                                self.from_text(intent="inform_country_code")]}


    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""

        flight_source = str(tracker.get_slot("fromloc.airport_code")).upper()
        flight_destination = str(tracker.get_slot("toloc.airport_code")).upper()
        departure_datetime = tracker.get_slot("time")
        departure_date = tracker.get_slot("depart_date")
        return_date = tracker.get_slot("return_date")
        no_of_adults = int(tracker.get_slot("no_of_adults"))
        no_of_children = int(tracker.get_slot("no_of_children"))
        no_of_infants = int(tracker.get_slot("no_of_infants"))
        class_type = tracker.get_slot("class_type")
        currency_code = tracker.get_slot("currency_code")
        round_trip = tracker.get_slot("round_trip")
        flight_stop = tracker.get_slot("flight_stop_check")
        title = tracker.get_slot("title")
        user_name = tracker.get_slot("user_name")
        email_id = tracker.get_slot("email_id")
        mobile_no = int(tracker.get_slot("mobile_no"))
        country_code = int(tracker.get_slot("country_code"))
        flight_stop_check = tracker.get_slot("flight_stop_check")

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

        if round_trip == "round trip":
            return_date = "Return date: "+tracker.get_slot("return_date")
        else:
            return_date = None

        out = "Checking information about available flights for the route {} --> {} on {} for {} {} {} in {} class. {}. The following flights are available: ".format(flight_source, flight_destination, str(departure_date)[:10], adults, children,
                                                                                                                                                                                      infants, class_type.title(), return_date)
        buttons = []

        try:
            global a
            a = AmadeusFlight(originLocation=flight_source, destinationLocation=flight_destination, departureDate=departure_date,returnDate=return_date,travelClass=class_type,adults=no_of_adults,children=no_of_children,infants=no_of_infants,currencyCode=currency_code,nonStop=flight_stop_check,title=title,user_name=user_name,email_id=email_id,mobile_no=mobile_no,country_code=country_code)
        except Exception as e:
            pass

        else:
            gfp = iter(a.generate_flight_quotes())
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
            dispatcher.utter_message(template="utter_no_flights_available")
            dispatcher.utter_message(template="utter_other_help")

        else:
            dispatcher.utter_message(text=out,buttons=buttons)
        return []


    def validate_no_of_adults(self,
                                value: float,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: Dict[Text, Any],
                                ) -> Dict[Text, Any]:

        if int(value) <= 0:
            dispatcher.utter_message("Atleast 1 adult should be travelling !")
            SlotSet("no_of_adults",None)
            return {"no_of_adults":None}

        else:
            return {"no_of_adults": value}

    def validate_child_passengers(self,
                                  value: bool,
                                  dispatcher: CollectingDispatcher,
                                  tracker: Tracker,
                                  domain: Dict[Text, Any],
                                  ) -> Dict[Text, Any]:

        if value:
            return {"child_passengers": value}

        else:
            SlotSet("no_of_children", 0)
            SlotSet("child_passengers", 0)
            return {"no_of_children": 0}

    def validate_infant_passengers(self,
                                   value: bool,
                                   dispatcher: CollectingDispatcher,
                                   tracker: Tracker,
                                   domain: Dict[Text, Any],
                                   ) -> Dict[Text, Any]:

        if value:
            return {"infant_passengers": value}

        else:
            SlotSet("no_of_infants", 0)
            SlotSet("infant_passengers", 0)
            return {"no_of_infants": 0}


    def validate_no_of_children(self,
                                value: float,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: Dict[Text, Any],
                                ) -> Dict[Text, Any]:

        if not(str(value).isdigit()) or int(value) <= 0:
            SlotSet("child_passengers", False)
            SlotSet("no_of_children", 0)
            return {"no_of_children":0}


        else:
            return {"no_of_children": value}


    def validate_no_of_infants(self,
                               value: float,
                               dispatcher: CollectingDispatcher,
                               tracker: Tracker,
                               domain: Dict[Text, Any],
                               ) -> Dict[Text, Any]:

        if int(value) > int(tracker.get_slot("no_of_adults")):
            dispatcher.utter_message("The number of infants must be less than or same as the number of adults")
            SlotSet("no_of_infants", None)
            return {"no_of_infants": None}

        if not(str(value).isdigit()) or int(value) <= 0:
            SlotSet("infant_passengers", False)
            SlotSet("no_of_infants", 0)
            return {"no_of_infants": 0}

        else:
            return {"no_of_infants": value}


    def validate_round_trip(self,
                                   value: Text,
                                   dispatcher: CollectingDispatcher,
                                   tracker: Tracker,
                                   domain: Dict[Text, Any],
                                   ) -> Dict[Text, Any]:
        """Validate round trip or one way value."""

        if value == "round trip":
            SlotSet("time",None)
            return {"round_trip": value}

        elif value == "one way":
            return {"round_trip": value}


    def validate_return_date(self,
                      value: Text,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain: Dict[Text, Any],
                      ) -> Dict[Text, Any]:
        """Validate return date."""


        if value:
            [return_date, return_time, *extra] =  re.split(r"[T,+,.]",tracker.get_slot("time"))
            return_date = datetime.strptime(return_date,"%Y-%m-%d").date()
            depart_date = datetime.strptime(tracker.get_slot("depart_date"),"%Y-%m-%d").date()
            if return_date < depart_date:
                dispatcher.utter_message("You need to choose a return date after the departure date")
                SlotSet("return_date",None)
                SlotSet("time",None)
                return {"return_date": None}
            else:
                SlotSet("return_date", str(return_date))
                return {"return_date": str(return_date)}

        else:
            SlotSet("return_date", str(return_date))
            return {"return_date": str(return_date)}


    # def validate_depart_date(self,
    #                   value: Text,
    #                   dispatcher: CollectingDispatcher,
    #                   tracker: Tracker,
    #                   domain: Dict[Text, Any],
    #                   ) -> Dict[Text, Any]:
    #     """Validate departure date."""
    #
    #     [depart_date, depart_time, *extra] =  re.split(r"[T,+,.]",tracker.get_slot("time"))
    #     depart_date = datetime.strptime(depart_date,"%Y-%m-%d").date()
    #     now = datetime.now().date()
    #
    #     if depart_date < now:
    #         dispatcher.utter_message("Sorry you need to choose date in the present for me to search for flights")
    #         SlotSet("depart_date",None)
    #         SlotSet("time",None)
    #         return {"depart_date": None}
    #     else:
    #         SlotSet("depart_date", str(depart_date))
    #         return {"depart_date": str(depart_date)}

    def validate_title(self,
                      value: Text,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain: Dict[Text, Any],
                      ) -> Dict[Text, Any]:
        """Validate departure date."""

        if value:
            SlotSet("title", value)
            return {"title": value}

        else:
            SlotSet("title", None)
            return {"title": None}


        # if value == "Mr":
        #     SlotSet("title", "Mr")
        #     return {"title": "Mr"}
        #
        # elif value == "Ms":
        #     SlotSet("title", "Ms")
        #     return {"title": "Ms"}
        #
        # elif value == "Mx":
        #     SlotSet("title", "Mx")
        #     return {"title": "Mx"}
        #
        # elif value == "Dr":
        #     SlotSet("title", "Dr")
        #     return {"title": "Dr"}

    # def validate_fromloc_city_name(self,
    #                   value: Text,
    #                   dispatcher: CollectingDispatcher,
    #                   tracker: Tracker,
    #                   domain: Dict[Text, Any],
    #                   ) -> Dict[Text, Any]:
    #     """Validate departure date."""
    #
    #     if value:
    #         city_name = tracker.get_slot("fromloc_city_name")
    #         city_iatas = list(get_city_iatas(city_name))
    #         if len(city_iatas) > 1:
    #             return [FollowupAction("ActionAskFromAirport")]
    #         else:
    #             SlotSet("fromloc_city_name", value)
    #             SlotSet("fromloc.airport_code", get_city_iata(value))
    #             return {"fromloc_city_name": value}
    #     else:
    #         SlotSet("fromloc_city_name", None)
    #         SlotSet("fromloc.airport_code", None)
    #         return {"fromloc_city_name": None}
    #
    #
    # def validate_toloc_city_name(self,
    #                   value: Text,
    #                   dispatcher: CollectingDispatcher,
    #                   tracker: Tracker,
    #                   domain: Dict[Text, Any],
    #                   ) -> Dict[Text, Any]:
    #     """Validate departure date."""
    #
    #     if value:
    #         city_name = tracker.get_slot("toloc_city_name")
    #         city_iatas = list(get_city_iatas(city_name))
    #         if len(city_iatas) > 1:
    #             return [FollowupAction("ActionAskToAirport")]
    #         else:
    #             SlotSet("toloc_city_name", value)
    #             SlotSet("toloc.airport_code", get_city_iata(value))
    #             return {"toloc_city_name": value}
    #     else:
    #         SlotSet("toloc_city_name", None)
    #         SlotSet("toloc.airport_code", None)
    #         return {"toloc_city_name": None}

    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Optional[List[EventType]]:
        """Request the next slot and utter template if needed,
            else return None"""

        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                if tracker.get_slot("fromloc_city_name") and not(tracker.get_slot("fromloc.airport_code")):
                    # dispatcher.utter_message(text="Did you mean..")
                    return [FollowupAction("action_ask_from_airport")]

                elif tracker.get_slot("toloc_city_name") and not(tracker.get_slot("toloc.airport_code")):
                    # dispatcher.utter_message(text="Did you mean..")
                    return [FollowupAction("action_ask_to_airport")]

                logger.debug(f"Request next slot '{slot}'")
                dispatcher.utter_message(template=f"utter_ask_{slot}", **tracker.slots)
                return [SlotSet(REQUESTED_SLOT, slot)]

        # no more required slots to fill
        return None

    def validate_time(self,
                      value: Text,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain: Dict[Text, Any],
                      ) -> Dict[Text, Any]:
        """Validate duckling time entity"""

        latest_intent = tracker.latest_message['intent'].get('name')

        if latest_intent == "flight":
            time_entities = [e for e in tracker.latest_message["entities"] if e["entity"] == "time"]
            if len(time_entities)>1:
                datetimes = [datetime.strptime(time_entities[0]["value"]["value"][:19],"%Y-%m-%dT%H:%M:%S"),datetime.strptime(time_entities[-1]["value"]["value"][:19],"%Y-%m-%dT%H:%M:%S")]
                depart_datetime, return_datetime = sorted(datetimes)
                depart_date = depart_datetime.date().strftime("%Y-%m-%d")
                depart_time = depart_datetime.time().strftime("%H:%M:%S")
                return_date = return_datetime.date().strftime("%Y-%m-%d")
                return_time = return_datetime.time().strftime("%H:%M:%S")
                SlotSet("depart_date",depart_date)
                SlotSet("return_date",return_date)
                return {"depart_date": depart_date, "return_date":return_date}

            else:
                [depart_date, depart_time, *extra] =  re.split(r"[T,+,.]",tracker.get_slot("time"))
                depart_date = datetime.strptime(depart_date,"%Y-%m-%d").date()
                now = datetime.now().date()
                if depart_date < now:
                    dispatcher.utter_message("Sorry you need to choose date in the present for me to search for flights")
                    SlotSet("depart_date",None)
                    SlotSet("time",None)
                    return {"depart_date": None}
                else:
                    SlotSet("depart_date", str(depart_date))
                    return {"depart_date": str(depart_date)}

        elif latest_intent == "inform_departure_date":
            [depart_date, depart_time, *extra] =  re.split(r"[T,+,.]",tracker.get_slot("time"))
            depart_date = datetime.strptime(depart_date,"%Y-%m-%d").date()
            now = datetime.now().date()

            if depart_date < now:
                dispatcher.utter_message("Sorry you need to choose date in the present for me to search for flights")
                SlotSet("depart_date",None)
                SlotSet("time",None)
                return {"depart_date": None}
            else:
                SlotSet("depart_date", str(depart_date))
                return {"depart_date": str(depart_date)}


        elif latest_intent == "inform_return_date":
            [return_date, return_time, *extra] =  re.split(r"[T,+,.]",tracker.get_slot("time"))
            return_date = datetime.strptime(return_date,"%Y-%m-%d").date()
            depart_date = tracker.get_slot("depart_date")
            depart_date = datetime.strptime(depart_date,"%Y-%m-%d").date()

            if return_date < depart_date:
                dispatcher.utter_message("You need to choose a return date after the departure date")
                SlotSet("return_date",None)
                SlotSet("time",None)
                return {"return_date": None}
            else:
                SlotSet("return_date", str(return_date))
                return {"return_date": str(return_date)}

        else:
            SlotSet("depart_date",None)
            return {"depart_date": None}



class FlightTimeForm(FormAction):
    """Custom form action to fill all slots required to find flight schedule or
    departure or arrival time for a route for a certain date."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "flight_time_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["fromloc_city_name", "toloc_city_name", "depart_date"]


    def slot_mappings(self) -> Dict[Text, Any]:
        return {"fromloc_city_name": self.from_entity(entity="fromloc_city_name",
                                                      intent=["flight_time","inform_departure_city"]),

                "toloc_city_name": self.from_entity(entity="toloc_city_name",
                                                    intent=["flight_time","inform_arrival_city"]),

                "depart_date": self.from_entity(entity="time",
                                                intent=["flight_time","inform_departure_date"]),

                "airline_name": self.from_entity(entity="airline_name",
                                                intent=["flight_time"]),

                "airline_code": self.from_entity(entity="airline_code",
                                                intent=["flight_time"]),

                "class_type": self.from_entity(entity="class_type",
                                               intent=["flight_time"]),

                "flight_time": self.from_entity(entity="flight_time",
                                               intent=["flight_time"]),

                "flight_mod": self.from_entity(entity="flight_mod",
                                               intent=["flight_time"]),

                "flight_stop": self.from_entity(entity="flight_stop",
                                               intent=["flight_time"]),

                "flight_number": self.from_entity(entity="flight_number",
                                               intent=["flight_time"]),

                "aircraft_code": self.from_entity(entity="aircraft_code",
                                               intent=["flight_time"]),

                "no_of_adults": self.from_entity(entity="no_of_adults",
                                                 intent=["flight_time"])}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""

        params = {}

        flight_source = tracker.get_slot("fromloc_city_name")
        flight_destination = tracker.get_slot("toloc_city_name")
        departure_date = tracker.get_slot("depart_date")
        airline_name = tracker.get_slot("airline_name")
        class_type = tracker.get_slot("class_type")
        flight_time = tracker.get_slot("flight_time")
        flight_mod = tracker.get_slot("flight_mod")
        flight_number = tracker.get_slot("flight_number")
        aircraft_code = tracker.get_slot("aircraft_code")
        params["originLocation"] = flight_source
        params["destinationLocation"] = flight_destination
        params["departureDate"] = departure_date
        params["flightTime"] = flight_time

        if no_of_adults:
            params["adults"] = int(no_of_adults)

        if class_type:
            params["travelClass"] = class_type

        if flight_mod:
            params["flightMod"] = flight_mod

        if tracker.get_slot("flight_stop") == "stop":
            params["nonStop"] = "true"

        if airline_name:
            airline_code = get_airline_iata(airline_name)
            params["includedAirlineCodes"] = airline_code

        elif airline_code:
            params["includedAirlineCodes"] = airline_code


        out = "Checking information about available flights for the route {} --> {} on {}. The following flights are available: ".format(flight_source, flight_destination, departure_date)
        buttons = []

        try:
            a = AmadeusFlight(**params)
        except Exception:
            pass

        else:
            gfp = iter(a.generate_flight_quotes())
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
            dispatcher.utter_message(template="utter_no_flights_available")
            dispatcher.utter_message(template="utter_other_help")
        else:
            dispatcher.utter_message(text=out,buttons=buttons)

        return []


    def validate_no_of_adults(self,
                                value: float,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: Dict[Text, Any],
                                ) -> Dict[Text, Any]:

        if int(value) <= 0:
            dispatcher.utter_message("Atleast 1 adult should be travelling !")
            SlotSet("no_of_adults",None)
            return {"no_of_adults":None}

        else:
            return {"no_of_adults": value}


    def validate_depart_date(self,
                      value: Text,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain: Dict[Text, Any],
                      ) -> Dict[Text, Any]:
        """Validate departure date."""

        [depart_date, depart_time, *extra] =  re.split(r"[T,+,.]",tracker.get_slot("time"))
        depart_date = datetime.strptime(depart_date,"%Y-%m-%d").date()
        now = datetime.now().date()

        if depart_date < now:
            dispatcher.utter_message("Sorry you need to choose date in the present for me to search for flights")
            SlotSet("depart_date",None)
            SlotSet("time",None)
            return {"depart_date": None}
        else:
            SlotSet("depart_date", str(depart_date))
            return {"depart_date": str(depart_date)}



        # if type(tracker.get_slot("time")) is dict:
        #     SlotSet("depart_date", tracker.get_slot("time")['from'])
        #     return {"depart_date": tracker.get_slot("time")['from']}
        # else:
        #     SlotSet("depart_date", tracker.get_slot("time"))
        #     return {"depart_date": tracker.get_slot("time")}




    # def validate_time(self,
    #                   value: Text,
    #                   dispatcher: CollectingDispatcher,
    #                   tracker: Tracker,
    #                   domain: Dict[Text, Any],
    #                   ) -> Dict[Text, Any]:
    #     """Validate duckling time entity"""
    #
    #     latest_intent = tracker.latest_message['intent'].get('name')
    #
    #     if latest_intent == "flight" or latest_intent == "inform_departure_date":
    #         [depart_date, depart_time, *extra] =  re.split(r"[T,+,.]",tracker.get_slot("time"))
    #         depart_date = datetime.strptime(depart_date,"%Y-%m-%d").date()
    #         now = datetime.now().date()
    #
    #         if depart_date < now:
    #             dispatcher.utter_message("Sorry you need to choose date in the present for me to search for flights")
    #             SlotSet("depart_date",None)
    #             SlotSet("time",None)
    #             return {"depart_date": None}
    #         else:
    #             SlotSet("depart_date", str(depart_date))
    #             return {"depart_date": str(depart_date)}
    #
    #     elif latest_intent == "inform_return_date":
    #         [return_date, return_time, *extra] =  re.split(r"[T,+,.]",tracker.get_slot("time"))
    #         return_date = datetime.strptime(return_date,"%Y-%m-%d").date()
    #         depart_datetime = tracker.get_slot("depart_date")
    #         depart_date = datetime.strptime(depart_datetime,"%Y-%m-%d").date()
    #
    #         if return_date < depart_date:
    #             dispatcher.utter_message("You need to choose a return date after the departure date")
    #             SlotSet("return_date",None)
    #             SlotSet("time",None)
    #             return {"return_date": None}
    #         else:
    #             SlotSet("return_date", str(return_date))
    #             return {"return_date": str(return_date)}



        # if value:
        #     time_val = re.split(r"[T,+,.]",str(value))[:2]
        #     if tracker.get_slot('return_flight'):
        #         return_date_val = time_val[0]
        #         return [SlotSet("return_date",return_date_val),SlotSet("time",None)]
        #
        #     else:
        #         depart_date_val = time_val[0]
        #         return [SlotSet("depart_date", depart_date_val),SlotSet("time",None)]
        #
        # else:
        #     return [SlotSet("time",None)]

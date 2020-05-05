# import requests
# import json
#
# url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/UK/GBP/en-GB/"
#
# querystring = {"query":"Stockholm"}
# headers = {
#     'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
#     'x-rapidapi-key': "5e95a68c99msh96592d58fcb9d95p17319bjsn5bcf6b61e6b5"
#     }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
# json_data = json.loads(response.text)
# depart_id = json_data["Places"][0]["PlaceId"]
#
# querystring = {"query":"Oslo"}
# response2 = requests.request("GET", url, headers=headers, params=querystring)
# json_data2 = json.loads(response2.text)
# arrival_id = json_data2["Places"][0]["PlaceId"]
#
#
# new_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/IN/INR/en-IN/{}/{}/2020-04-01".format(depart_id,arrival_id)
# new_querystring = {"inboundpartialdate":"2020-02-27"}
# response3 = requests.request("GET", new_url, headers=headers, params=new_querystring)
# json_data3 = json.loads(response3.text)
# price = json_data3["Quotes"][0]["MinPrice"]
# print(price)

from amadeus_endpoint import AmadeusFlight
from iata_mapping import get_city_name, get_airline_name
import re

try:
    a = AmadeusFlight("Pune", "Delhi", "2020-07-01")
except Exception as e:
    dispatcher.utter_message(str(e))
else:
    res = a.generate_flight_prices()
    quote_id = 0
    for data in res:
        for itinerary in data["itineraries"]:
            departure = itinerary["segments"][0]["departure"]
            departure_place = get_city_name(departure["iataCode"])
            departure_datetime = departure["at"].split("T")
            departure_date = departure_datetime[0]
            departure_time = departure_datetime[1]
            try:
                departure_terminal = departure["terminal"]
            except KeyError:
                departure_terminal = ""
            arrival = itinerary["segments"][-1]["arrival"]
            arrival_place = get_city_name(arrival["iataCode"])
            arrival_datetime = arrival["at"].split("T")
            arrival_date = arrival_datetime[0]
            arrival_time = arrival_datetime[1]
            try:
                arrival_terminal = arrival["terminal"]
            except KeyError as e:
                arrival_terminal = ""
            airline_iata_code = itinerary["segments"][0]["carrierCode"]
            airline_name = get_airline_name(airline_iata_code)
            flight_duration = re.split(r"[PT,H,M]", itinerary["segments"][0]["duration"])
            hours = flight_duration[2]
            minutes = flight_duration[3]
            output = "{} flight Departure from {},{} {} at {} \t ---> \t Arrival in {},{} {} at {}.".format(airline_name, departure_place, "Terminal: " + departure_terminal if departure_terminal != "" else "", departure_date,
                                                                                                            departure_time, arrival_place, "Terminal: " + arrival_terminal if arrival_terminal != "" else "", arrival_date, arrival_time)
            output = output + " Duration: {} hours and {} minutes".format(
                hours, minutes) if minutes != '' else output + " Duration: {} hours".format(hours)
            print(output)

#print(get_city_name("BOM"))


# class ActionFlightSearch(Action):
#
#     def name(self) -> Text:
#         return "action_flight_search"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         flight_source = tracker.get_slot("fromloc.city_name")
#         flight_destination = tracker.get_slot("toloc.city_name")
#         departure_datetime = tracker.get_slot("time")
#
#         depart_id = get_place_id(flight_source)
#         arrival_id = get_place_id(flight_destination)
#         json_data = get_routes(depart_id,arrival_id,str(departure_datetime)[:10])
#         prices = json_data["Quotes"]
#         buttons = []
#
#         if prices:
#             for price in prices:
#                 carrier_id = price["OutboundLeg"]["CarrierIds"][0]
#                 carrier_name = list(filter(lambda x: x["CarrierId"] == carrier_id, json_data["Carriers"]))[0]["Name"]
#                 buttons.append({"title":"Airline : {}, Price : ₹{}, Departure Time : {} ".format(carrier_name,price["MinPrice"],price["QuoteDateTime"][-8:]),"payload":"/quote{\"quote_id\":\""+str(price["QuoteId"])+"\"}"})
#             dispatcher.utter_message(text="Checking about available flights for that route {} to {}. The following flights are available: ".format(flight_source,flight_destination),buttons=buttons)
#         else:
#             dispatcher.utter_message("No flights available for that route")
#         return []

# class ActionFlightSearch(Action):
#
#     def name(self) -> Text:
#         return "action_flight_search"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         flight_source = tracker.get_slot("fromloc.city_name")
#         flight_destination = tracker.get_slot("toloc.city_name")
#         departure_datetime = tracker.get_slot("depart_date")
#         buttons = []
#
#         try:
#             a = AmadeusFlight(flight_source, flight_destination,
#                               str(departure_datetime)[:10])
#         except Exception:
#             pass
#
#         else:
#             gfp = iter(a.generate_flight_prices())
#             quote_id = 1
#
#             while True:
#                 try:
#                     output = next(gfp)
#                     buttons.append(
#                         {"title": output, "payload": "/quote{\"quote_id\":\"" + str(quote_id) + "\"}"})
#                     quote_id = quote_id + 1
#                 except StopIteration:
#                     quote_id = 1
#                     break
#
#         if len(buttons) == 0:
#             dispatcher.utter_message("No flights available for that route")
#             return []
#         else:
#             dispatcher.utter_message(text="Checking about available flights for that route {} to {}. The following flights are available: ".format(
#                 flight_source, flight_destination), buttons=buttons)
#
#         return []


# [
#     {"body":"on 8th September","start":22,"value":
#         {"values":[
#                     {"value":"2020-09-08T00:00:00.000-07:00","grain":"day","type":"value"},
#                     {"value":"2021-09-08T00:00:00.000-07:00","grain":"day","type":"value"},
#                     {"value":"2022-09-08T00:00:00.000-07:00","grain":"day","type":"value"}
#                   ],
#          "value":"2020-09-08T00:00:00.000-07:00","grain":"day","type":"value"
#         },
#          "end":38,"dim":"time","latent":False
#     },
#
#     {"body":"on 18th November","start":50,"value":
#         {"values":[
#                     {"value":"2020-11-18T00:00:00.000-08:00","grain":"day","type":"value"},
#                     {"value":"2021-11-18T00:00:00.000-08:00","grain":"day","type":"value"},
#                     {"value":"2022-11-18T00:00:00.000-08:00","grain":"day","type":"value"}
#                   ],
#         "value":"2020-11-18T00:00:00.000-08:00","grain":"day","type":"value"
#         }
#     }
# ]


# {
#     "intent": {
#         "name": "inform_return_date",
#         "confidence": 0.9012346267700195
#     },
#     "entities": [
#         {
#             "start": 20,
#             "end": 24,
#             "value": "13th",
#             "entity": "return_date.day_number",
#             "confidence": 0.5734733990198869,
#             "extractor": "CRFEntityExtractor"
#         },
#         {
#             "start": 25,
#             "end": 32,
#             "value": "October",
#             "entity": "return_date.month_name",
#             "confidence": 0.442162783340129,
#             "extractor": "CRFEntityExtractor"
#         },
#         {
#             "start": 37,
#             "end": 43,
#             "value": "round trip",
#             "entity": "round_trip",
#             "confidence": 0.7409239509044201,
#             "extractor": "CRFEntityExtractor",
#             "processors": [
#                 "EntitySynonymMapper"
#             ]
#         },
#         {
#             "start": 47,
#             "end": 51,
#             "value": "19th",
#             "entity": "return_date.day_number",
#             "confidence": 0.907452509781391,
#             "extractor": "CRFEntityExtractor"
#         },
#         {
#             "start": 52,
#             "end": 60,
#             "value": "November",
#             "entity": "return_date.month_name",
#             "confidence": 0.8947719418357718,
#             "extractor": "CRFEntityExtractor"
#         },
#         {
#             "start": 17,
#             "end": 32,
#             "text": "on 13th October",
#             "value": "2020-10-13T00:00:00.000+00:00",
#             "confidence": 1.0,
#             "additional_info": {
#                 "values": [
#                     {
#                         "value": "2020-10-13T00:00:00.000+00:00",
#                         "grain": "day",
#                         "type": "value"
#                     },
#                     {
#                         "value": "2021-10-13T00:00:00.000+00:00",
#                         "grain": "day",
#                         "type": "value"
#                     },
#                     {
#                         "value": "2022-10-13T00:00:00.000+00:00",
#                         "grain": "day",
#                         "type": "value"
#                     }
#                 ],
#                 "value": "2020-10-13T00:00:00.000+00:00",
#                 "grain": "day",
#                 "type": "value"
#             },
#             "entity": "time",
#             "extractor": "DucklingHTTPExtractor"
#         },
#         {
#             "start": 44,
#             "end": 60,
#             "text": "on 19th November",
#             "value": "2020-11-19T00:00:00.000+00:00",
#             "confidence": 1.0,
#             "additional_info": {
#                 "values": [
#                     {
#                         "value": "2020-11-19T00:00:00.000+00:00",
#                         "grain": "day",
#                         "type": "value"
#                     },
#                     {
#                         "value": "2021-11-19T00:00:00.000+00:00",
#                         "grain": "day",
#                         "type": "value"
#                     },
#                     {
#                         "value": "2022-11-19T00:00:00.000+00:00",
#                         "grain": "day",
#                         "type": "value"
#                     }
#                 ],
#                 "value": "2020-11-19T00:00:00.000+00:00",
#                 "grain": "day",
#                 "type": "value"
#             },
#             "entity": "time",
#             "extractor": "DucklingHTTPExtractor"
#         }
#     ]
# }

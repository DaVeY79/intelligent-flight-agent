from amadeus import Client, ResponseError
from iata_mapping import get_city_name, get_city_iata
import re

amadeus = Client(
    client_id='6QQLRW6rZxxWehfqpoPXEOfkq2e6wCeB',
    client_secret='bMQBEJK4y65keE5z')

class AmadeusFlight:
    def __init__(self,originLocation, destinationLocation, departureDate, returnDate=None, adults=1, children=0, infants=0, travelClass=None, includedAirlineCodes=None, maxPrice=None, currencyCode="INR", nonStop="false",max=5):
        self.originLocationCode = get_city_iata(originLocation)
        self.destinationLocationCode = get_city_iata(destinationLocation)
        self.departureDate = departureDate
        self.adults = adults

        params = {}
        params["originLocationCode"] = self.originLocationCode
        params["destinationLocationCode"] = self.destinationLocationCode
        params["departureDate"] = self.departureDate
        params["adults"] = adults
        params["children"] = children
        params["infants"] = infants
        #params["nonStop"] = nonStop
        params["currencyCode"] = currencyCode
        params["max"] = max

        if returnDate:
            params["returnDate"] = returnDate

        if travelClass:
            params["travelClass"] = travelClass

        if includedAirlineCodes:
            params["includedAirlineCodes"] = includedAirlineCodes

        if maxPrice:
            params["maxPrice"] = maxPrice

        try:
            # response = amadeus.shopping.flight_offers_search.get(originLocationCode=self.originLocationCode,destinationLocationCode=self.destinationLocationCode,departureDate=self.departureDate,adults=self.adults)
            response = amadeus.shopping.flight_offers_search.get(**params)
            self.res = response.data
        except ResponseError as error:
            raise Exception("No flights available for that route")

    def generate_flight_prices(self):
        for data in self.res:
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
                # airline_name = get_airline_name(airline_iata_code)
                airline_name = amadeus.reference_data.airlines.get(airlineCodes=airline_iata_code).data[0]["commonName"]
                flight_duration = re.split(r"[PT,H,M]", itinerary["segments"][0]["duration"])
                hours = flight_duration[2]
                minutes = flight_duration[3]
                output = "{} flight Departure from {},{} {} at {} --->  Arrival in {},{} {} at {}.".format(airline_name, departure_place, "Terminal: " + departure_terminal if departure_terminal != "" else "", departure_date,
                                                                                                                departure_time, arrival_place, "Terminal: " + arrival_terminal if arrival_terminal != "" else "", arrival_date, arrival_time)
                output = output + " Duration: {} hours and {} minutes".format(
                    hours, minutes) if minutes != '' else output + " Duration: {} hours".format(hours)

                yield output

# a = AmadeusFlight(originLocation="Bangalore",destinationLocation="Dubai",departureDate="2020-10-05",adults=3,children=3,infants=2,travelClass="ECONOMY",currencyCode="INR")
# gfp = iter(a.generate_flight_prices())

# while True:
#     try:
#         output = next(gfp)
#         print(output)
#     except StopIteration:
#         break

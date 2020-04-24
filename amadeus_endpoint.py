from amadeus import Client, ResponseError
from iata_mapping import get_city_name, get_city_iata
import re


res = 0

amadeus = Client(
    client_id='6QQLRW6rZxxWehfqpoPXEOfkq2e6wCeB',
    client_secret='bMQBEJK4y65keE5z'
)


def generate_flight_prices():
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
            airline_name = amadeus.reference_data.airlines.get(
                airlineCodes=airline_iata_code).data[0]['commonName'].title()
            flight_duration = re.split(
                r"[PT,H,M]", itinerary["segments"][0]["duration"])
            hours = flight_duration[2]
            minutes = flight_duration[3]
            yield (airline_name, departure_place, departure_terminal, departure_date, departure_time, arrival_place, arrival_terminal, arrival_date, arrival_time, hours, minutes)


def get_flight_offers(originLocation, destinationLocation, departureDate, returnDate=None, adults=1, children=None, infants=None, travelClass="ECONOMY", includedAirlineCodes=[], nonStop=True):
    global res
    try:
        response = amadeus.shopping.flight_offers_search.get(originLocationCode=get_city_iata(
            originLocation), destinationLocationCode=get_city_iata(destinationLocation), departureDate=departureDate, adults=1)
        res = response.data
    except ResponseError as error:
        print(error)

    gfp = iter(generate_flight_prices())

    while True:
        try:
            (airline_name, departure_place, departure_terminal, departure_date, departure_time,
             arrival_place, arrival_terminal, arrival_date, arrival_time, hours, minutes) = next(gfp)
            output = "{} flight Departure from {},{} {} at {} \t ---> \t Arrival in {},{} {} at {}.".format(airline_name, departure_place, "Terminal: " + departure_terminal if departure_terminal != "" else "", departure_date,
                                                                                                            departure_time, arrival_place, "Terminal: " + arrival_terminal if arrival_terminal != "" else "", arrival_date, arrival_time)
            output = output + " Duration: {} hours and {} minutes".format(
                hours, minutes) if minutes != '' else output + " Duration: {} hours".format(hours)
            print(output)
        except StopIteration:
            break


get_flight_offers("Pune", "Delhi", "2020-07-01")
# print(get_city_iata("Delhi"))

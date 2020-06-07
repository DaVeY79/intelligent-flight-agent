from amadeus import Client, ResponseError
from datetime import datetime
from iata_mapping import get_city_name, get_city_iata, get_airline_name, get_airport_name
import re
import calendar
import logging
from sqlalchemy import create_engine, MetaData, Table, insert, select
import mysql.connector
import uuid
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
from python_http_client.exceptions import HTTPError
import os
import configparser


# logger = logging.getLogger('your_logger')
# logger.setLevel(logging.DEBUG)
config = configparser.ConfigParser()
config.read('config.ini')
amadeus_client_id = config["amadeus"]["client_id"]
amadeus_client_secret = config["amadeus"]["client_secret"]
db_user = config["database"]["user"]
db_password = config["database"]["password"]
db_hostname = config["database"]["hostname"]
db_name = config["database"]["dbname"]
db_port = config["database"]["port"]
oneway_template_id = config["sendgrid"]["template_id_one_way"]
roundtrip_template_id = config["sendgrid"]["template_id_round_trip"]
sendgrid_api_key = config["sendgrid"]["api_key"]
sendgrid_from_email = config["sendgrid"]["from_email"]

db_connection_string = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(db_user,db_password,db_hostname,db_port,db_name)


amadeus = Client(
    client_id=amadeus_client_id,
    client_secret=amadeus_client_secret
    # logger=logger
)

currency_code_mapping = {"USD": ["US Dollars","$"], "EUR": ["Euros","€"], "JPY": ["Japanese Yen","¥"], "GBP": ["Pound Sterling","£"], "CHF": ["Swiss Francs","₣"],
                         "INR": ["Indian Rupees","₹"], "AUD": ["Australian Dollars","Aus$"], "CAD": ["Canadian Dollars","Can$"], "CNY": ["Chinese Yuan Renminbi","￥"]}


class AmadeusFlight:
    def __init__(self, originLocation, destinationLocation, departureDate, returnDate=None, adults=1, children=0, infants=0, travelClass=None,
                 includedAirlineCodes=None, maxPrice=None, flightmod=None, flight_time=None, email_id=None, mobile_no=None, country_code=None,
                 title=None, user_name=None, currencyCode="INR", nonStop="false", max=5):

        self.originLocationCode = originLocation
        self.destinationLocationCode = destinationLocation
        self.departureDate = departureDate
        self.adults = adults
        self.children = children
        self.infants = infants
        self.currencyCode = currencyCode
        self.travelClass = travelClass
        self.title = title
        self.user_name = user_name
        self.email_id = email_id
        self.mobile_no = mobile_no
        self.country_code = country_code
        self.return_date = returnDate

        params = {}
        params["originLocationCode"] = self.originLocationCode
        params["destinationLocationCode"] = self.destinationLocationCode
        params["departureDate"] = departureDate
        params["adults"] = adults
        params["children"] = children
        params["infants"] = infants
        params["nonStop"] = nonStop
        params["currencyCode"] = currencyCode
        params["max"] = max

        if self.return_date:
            params["returnDate"] = returnDate

        if travelClass != "ANY_CLASS" and travelClass:
            params["travelClass"] = travelClass

        if includedAirlineCodes:
            params["includedAirlineCodes"] = includedAirlineCodes

        if maxPrice:
            params["maxPrice"] = maxPrice

        try:
            response = amadeus.shopping.flight_offers_search.get(**params)
            self.res = response.data
        except ResponseError as error:
            raise Exception("No flights available for that route")
        else:
            self.engine = create_engine(db_connection_string, encoding="utf-8", echo = False)
            metadata = MetaData()
            self.bookings = Table("bookings",metadata,autoload=True,autoload_with=self.engine)

    def generate_flight_quotes(self):
        for data in self.res:
            itinerary_out = ""
            for itinerary_no, itinerary in enumerate(data["itineraries"]):
                segment_fare_details = list(
                    filter(lambda x: x['travelerType'] == 'ADULT', data['travelerPricings']))[0]
                baggage_allowance = segment_fare_details['fareDetailsBySegment'][-1]['includedCheckedBags']
                if baggage_allowance.get("weight"):
                    baggage_allowance_str = str(baggage_allowance["weight"]) + baggage_allowance["weightUnit"]
                else:
                    baggage_allowance_str = "25kg"
                stops_str = self.stops_format(itinerary["segments"])
                departure = itinerary["segments"][0]["departure"]
                departure_place = get_city_name(departure["iataCode"])
                departure_date, departure_time = self.datetime_format(
                    departure["at"])
                departure_terminal = "(Terminal: {})".format(
                    departure.get("terminal")).replace("(Terminal: None)", "")
                arrival = itinerary["segments"][-1]["arrival"]
                arrival_place = get_city_name(arrival["iataCode"])
                arrival_date, arrival_time = self.datetime_format(
                    arrival["at"])
                arrival_terminal = "(Terminal: {})".format(
                    arrival.get("terminal")).replace("(Terminal: None)", "")
                airline_iata_code = itinerary["segments"][0]["carrierCode"]
                # airline_name = get_airline_name(airline_iata_code)
                airline_name = amadeus.reference_data.airlines.get(
                    airlineCodes=airline_iata_code).data[0]["businessName"].title()
                flight_duration = self.duration_format(itinerary["duration"])
                price = data["price"]
                total_cost = currency_code_mapping.get(price["currency"])[1]+price["grandTotal"]
                if itinerary_no%2 == 0:
                    trip_leg = "Outbound journey: "
                else:
                    trip_leg = "Inbound journey: "
                output = "{} {} Departure from {}{} on {} at {} --->  Arrival in {}{} on {} at {}. {}. {}. Cost: {}. Baggage Allowance : {}.\n".format(trip_leg, airline_name, departure_place, departure_terminal, departure_date,
                                                                                                                                                    departure_time, arrival_place, arrival_terminal, arrival_date, arrival_time, flight_duration, stops_str, total_cost, baggage_allowance_str)
                itinerary_out += output

            yield itinerary_out

    def confirm_pricing(self, quote_id):
        self.confirm_offer = amadeus.shopping.flight_offers.pricing.post(
            self.res[quote_id - 1])

    def generate_flight_timings_weekday(self):
        for data in self.res:
            for itinerary_no, itinerary in enumerate(data["itineraries"]):
                stops_str = self.stops_format(itinerary["segments"])
                departure = itinerary["segments"][0]["departure"]
                departure_place = get_city_name(departure["iataCode"])
                departure_date, departure_time = self.datetime_format(departure["at"])
                departure_terminal = "(Terminal: {})".format(departure.get("terminal")).replace("(Terminal: None)", "")
                arrival = itinerary["segments"][-1]["arrival"]
                arrival_place = get_city_name(arrival["iataCode"])
                arrival_date, arrival_time = self.datetime_format(arrival["at"])
                arrival_terminal = "(Terminal: {})".format(arrival.get("terminal")).replace("(Terminal: None)", "")
                airline_iata_code = itinerary["segments"][0]["carrierCode"]
                airline_name = amadeus.reference_data.airlines.get(airlineCodes=airline_iata_code).data[0]["businessName"].title()
                flight_duration = self.duration_format(itinerary["duration"])

                if itinerary_no%2 == 1:
                    trip_leg = "Outbound journey: "
                else:
                    trip_leg = "Inbound journey: "

                output = self.flight_time_format(trip_leg, airline_name, departure_place, departure_terminal, departure_date,
                                                 departure_time, arrival_place, arrival_terminal, arrival_date, arrival_time, flight_duration, stops_str)

                if datetime.strptime(departure_time, "%I:%M %p").weekday() < 5:
                    yield output

    def generate_flight_timings_relative(self):
        timings = []
        for data in self.res:
            for itinerary_no, itinerary in enumerate(data["itineraries"]):
                stops_str = self.stops_format(itinerary["segments"], segment_fare_details)
                departure = itinerary["segments"][0]["departure"]
                departure_place = get_city_name(departure["iataCode"])
                departure_date, departure_time = self.datetime_format(departure["at"])
                departure_terminal = "(Terminal: {})".format(departure.get("terminal")).replace("(Terminal: None)", "")
                arrival = itinerary["segments"][-1]["arrival"]
                arrival_place = get_city_name(arrival["iataCode"])
                arrival_date, arrival_time = self.datetime_format(arrival["at"])
                arrival_terminal = "(Terminal: {})".format(arrival.get("terminal")).replace("(Terminal: None)", "")
                airline_iata_code = itinerary["segments"][0]["carrierCode"]
                airline_name = amadeus.reference_data.airlines.get(airlineCodes=airline_iata_code).data[0]["businessName"].title()
                flight_duration = self.duration_format(itinerary["duration"])

                if itinerary_no%2 == 1:
                    trip_leg = "Outbound journey: "
                else:
                    trip_leg = "Inbound journey: "

                output = self.flight_time_format(trip_leg, airline_name, departure_place, departure_terminal, departure_date,
                                                 departure_time, arrival_place, arrival_terminal, arrival_date, arrival_time, flight_duration, stops_str)

                timings.append((output, datetime.strptime(departure_time, "%I:%M %p"), datetime.strptime(arrival_time, "%I:%M %p")))

        if self.flight_mod == "early":
            output = min(timings, key=lambda x: x[1])
            yield output[0]

        elif self.flight_mod == "last":
            output = max(timings, key=lambda x: x[1])
            yield output[0]

        elif self.flight_mod == "earliest arriving":
            output = min(timings, key=lambda x: x[2])
            yield output[0]

    def flight_time_format(self, trip_leg, airline_name, departure_place, departure_terminal, departure_date,
                           departure_time, arrival_place, arrival_terminal, arrival_date, arrival_time, flight_duration, stops_str):

        if self.flight_time == "flight time":
            return "{} {} Departure from {}{} on {} at {} --->  Arrival in {}{} on {} at {}. {}. {}".format(trip_leg, airline_name, departure_place, departure_terminal, departure_date, departure_time, arrival_place, arrival_terminal, arrival_date, arrival_time, flight_duration, stops_str)

        elif self.flight_time == "departure time":
            return "{} {} Departure from {}{} on {} at {}. {}. {}".format(trip_leg, airline_name, departure_place, departure_terminal, departure_date, departure_time, flight_duration, stops_str)

        elif self.flight_time == "arrival time":
            return "{} {} Arrival in {}{} on {} at {}. {}. {}".format(trip_leg, airline_name, arrival_place, arrival_terminal, arrival_date, arrival_time, flight_duration, stops_str)

    def insert_booking_details(self,quote_id):
        quote = self.res[quote_id]
        prices = amadeus.shopping.flight_offers.pricing.post(quote).data
        itineraries = quote["itineraries"]
        outbound = itineraries[0]
        values_list = []
        # outbound_prices = prices["flightOffers"][0]["itineraries"][0]
        # inbound_prices = prices["flightOffers"][0]["itineraries"][1]
        pnr = self.get_pnr()
        if self.return_date:
            self.round_trip=True
            inbound = itineraries[1]
            self.inbound_params = self.get_booking_params(pnr,prices,quote,inbound,"in")
            values_list.append(self.inbound_params)
        else:
            self.round_trip=False

        self.outbound_params = self.get_booking_params(pnr,prices,quote,outbound,"out")
        values_list.append(self.outbound_params)

        send_email = self.send_email_confirmation(self.outbound_params,pnr)
        with self.engine.connect() as connection:
            try:
                query = insert(self.bookings, inline = False)
                ResultProxy = connection.execute(query,values_list)
            except Exception as e:
                print(e)

        return pnr


    def get_pnr(self):
        return "PNR"+str(uuid.uuid4().hex[:4])

    def get_booking_params(self, pnr,prices, quote, travel_leg,travel_bound):
        booking_params = {}
        pnr_bound_extension = {"in":"IB","out":"OB"}
        booking_params["pnr"] = pnr+pnr_bound_extension.get(travel_bound)
        booking_params["booking_date"] = datetime.now().strftime("%Y-%m-%d")
        departure = travel_leg["segments"][0]["departure"]
        booking_params["source_iata"] = departure["iataCode"]
        booking_params["source_terminal"] = departure.get("terminal")
        arrival = travel_leg["segments"][-1]["arrival"]
        booking_params["destination_iata"] = arrival["iataCode"]
        booking_params["destination_terminal"] = arrival.get("terminal")
        stops = {"segments":travel_leg["segments"]}
        if self.round_trip:
            booking_params["stops"] = str(json.dumps(stops))
        booking_params["no_of_stops"] = len(travel_leg["segments"])-1
        booking_params["flight_number"] = travel_leg["segments"][0]["number"]
        booking_params["aircraft_type"] = travel_leg["segments"][0]["aircraft"]["code"]
        booking_params["depart_date"], booking_params["depart_time"] = departure["at"].split("T")
        booking_params["arrive_date"], booking_params["arrive_time"] = arrival["at"].split("T")
        segment_fare_details = list(filter(lambda x: x['travelerType'] == 'ADULT', prices.get('flightOffers')[0].get('travelerPricings')))[0]
        baggage_allowance = segment_fare_details['fareDetailsBySegment'][-1]['includedCheckedBags']
        if baggage_allowance.get("weight"):
            booking_params["baggage_allowance_weight"] = int(baggage_allowance.get("weight"))
            booking_params["baggage_allowance_unit"] = baggage_allowance.get("weightUnit")
        else:
            booking_params["baggage_allowance_weight"] = 25
            booking_params["baggage_allowance_unit"] = "kg"
        if baggage_allowance.get("no_of_checkbags"):
            booking_params["no_of_checkbags"] = baggage_allowance.get("quantity")
        else:
            booking_params["no_of_checkbags"] = 2
        booking_params["airline_iata"] = travel_leg["segments"][0]["carrierCode"]
        booking_params["flight_duration"] = self.duration_format(travel_leg["duration"]).replace(" Total duration: ","")
        booking_params["travel_class"] = self.travelClass
        booking_params["adult_paxno"] = int(self.adults)
        booking_params["child_paxno"] = int(self.children)
        booking_params["infant_paxno"] = int(self.infants)
        booking_params["currency"] = self.currencyCode
        booking_params["base_fare"] = float(prices.get('flightOffers')[0].get('price').get('base'))
        booking_params["supplier_fee"] = float(list(filter(lambda x:x["type"] == "SUPPLIER", prices["flightOffers"][0]["price"]["fees"]))[0]["amount"])
        booking_params["ticketing_fee"] = float(list(filter(lambda x:x["type"] == "TICKETING", prices["flightOffers"][0]["price"]["fees"]))[0]["amount"])
        booking_params["form_of_payment_fee"] = float(list(filter(lambda x:x["type"] == "FORM_OF_PAYMENT", prices["flightOffers"][0]["price"]["fees"]))[0]["amount"])
        total_tax = 0.0
        for traveler in prices.get("flightOffers")[0].get("travelerPricings"):
            if traveler.get("price").get("taxes"):
                for tax in traveler.get("price").get("taxes"):
                    total_tax += float(tax.get("amount"))
        booking_params["fare_basis_code"] = prices.get("flightOffers")[0].get("travelerPricings")[0].get('fareDetailsBySegment')[0].get("fareBasis")
        booking_params["tax"] = total_tax
        booking_params["travel_bound"] = travel_bound
        booking_params["email_id"] = self.email_id
        booking_params["mobile_no"] = self.mobile_no
        booking_params["country_code"] = self.country_code
        booking_params["title"] = self.title
        booking_params["user_name"] = self.user_name
        # print(booking_params)
        return booking_params

    def get_email_params(self,booking_params, pnr):
        email_params = {k:booking_params[k] for k in ["pnr","base_fare","supplier_fee","ticketing_fee","form_of_payment_fee","tax","email_id","mobile_no","country_code","no_of_checkbags"]}
        email_params["airline_name"] = "<strong>"+amadeus.reference_data.airlines.get(airlineCodes=booking_params["airline_iata"]).data[0]["businessName"].title()+"</strong>"
        email_params["airline_iata"] = "<strong>"+booking_params["airline_iata"]+"</strong>"
        email_params["baggage_allowance"] = str(booking_params["baggage_allowance_weight"])+booking_params["baggage_allowance_unit"].lower()
        email_params["user_name"] = booking_params["title"]+". "+booking_params["user_name"]
        email_params["total"] = booking_params["base_fare"]+booking_params["supplier_fee"]+booking_params["ticketing_fee"]+booking_params["form_of_payment_fee"]+booking_params["tax"]
        email_params["outbound"] = {
                                    "source_place" : get_city_name(self.outbound_params["source_iata"]),
                                    "source_airport" : get_airport_name(self.outbound_params["source_iata"]),
                                    "destination_place" : get_city_name(self.outbound_params["destination_iata"]),
                                    "destination_airport" : get_airport_name(self.outbound_params["destination_iata"]),
                                    "depart_date" : datetime.strptime(self.outbound_params["depart_date"],"%Y-%m-%d").strftime("%a, %d %b %Y"),
                                    "depart_time" : self.outbound_params["depart_time"][:5],
                                    "arrive_time" : self.outbound_params["arrive_time"][:5],
                                    "no_of_stops" : self.outbound_params["no_of_stops"],
                                    "flight_no" : self.outbound_params["flight_number"],
                                    "flight_duration" : self.outbound_params["flight_duration"]
                                    }
        if self.round_trip:
            email_params["inbound"] = {
                                        "source_place" : get_city_name(self.inbound_params["source_iata"]),
                                        "destination_place" : get_city_name(self.inbound_params["destination_iata"]),
                                        "depart_date" : datetime.strptime(self.inbound_params["depart_date"],"%Y-%m-%d").strftime("%a, %d %b %Y"),
                                        "depart_time" : self.inbound_params["depart_time"][:5],
                                        "arrive_time" : self.inbound_params["arrive_time"][:5],
                                        "no_of_stops" : self.inbound_params["no_of_stops"],
                                        "flight_no" : self.inbound_params["flight_number"],
                                        "flight_duration" : self.inbound_params["flight_duration"]
                                        }
        # print(email_params)

        return email_params

    def send_email_confirmation(self,booking_params,pnr):
        data = self.get_email_params(booking_params,pnr)
        log = logging.getLogger(__name__)
        message = Mail(from_email=sendgrid_from_email,
                       to_emails=booking_params["email_id"],
                       subject='TravelAgentBot: Flight booking confirmation')
        if self.round_trip:
            message.template_id = roundtrip_template_id
        else:
            message.template_id = oneway_template_id
        message.dynamic_template_data = data
        try:
            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(message)
            log.info(f"email.status_code={response.status_code}")
        except HTTPError as e:
            log.error(e)


    def generate_flight_round_trip_quotes(self):
        gfp = iter(self.generate_flight_quotes())
        quote = 1
        while True:
            try:
                out = "Onward journey: {}\nReturn journey: {}".format(
                    next(gfp), next(gfp))
                #quote += 1
                yield out
            except StopIteration:
                return None

    def duration_format(self, time):
        time_val = [s for s in re.split(r"[PT,H,M]", time) if s.isdigit()]
        if "H" in time and len(time_val) == 1:
            hours = time_val[0]
            return " Total duration: {}h".format(hours)
        elif "M" in time and len(time_val) == 1:
            minutes = time_val[0]
            return " Total duration: {}m".format(minutes)
        else:
            hours, minutes = time_val
            return " Total duration: {}h and {}m".format(hours, minutes)

    def datetime_format(self, date_time):
        date, time = date_time.split("T")
        date = datetime.strptime(
            date, "%Y-%m-%d").strftime("%B %d, %Y").lstrip("0").replace(" 0", " ")
        time = datetime.strptime(time, "%H:%M:%S").strftime(
            "%I:%M %p").lstrip("0").replace(" 0", " ")
        return [date, time]

    def stops_format(self, segments):
        stops = []
        no_of_segments = len(segments)
        if no_of_segments > 2:
            stop_no = 1
            for segment in segments[:-1]:
                segment_id = segment["id"]
                [date, time] = self.datetime_format(segment["arrival"]["at"])
                stops.append("{}.{} at {} on {}".format(
                    stop_no, get_city_name(segment["arrival"]["iataCode"]), time, date))
                stop_no += 1
            stops_str = "{} stops at: ".format(no_of_segments - 1)
            stops_str += " and ".join([",".join(stops[:-1]), stops[-1]])
        elif no_of_segments == 2:
            segment = segments[0]
            [date, time] = self.datetime_format(segment["arrival"]["at"])
            stops.append("{} at {} on {}".format(get_city_name(
                segment["arrival"]["iataCode"]), time, date.replace(",", "")))
            stops_str = "1 stop at: {}".format(stops[0])
        else:
            stops_str = ""
        return stops_str

# if __name__ == "__main__":
#     a = AmadeusFlight(originLocation="DXB", destinationLocation="AKL", departureDate="2020-10-05",
#                     adults=3, children=3, infants=2, travelClass="ANY_CLASS", currencyCode="EUR",
#                      title="Mr.", user_name="Arnold Schwarznegger",email_id="david@daveabraham.me",mobile_no=9850369780,country_code=91)

    # gfp = iter(a.generate_flight_quotes())
    # while True:
    #     try:
    #         output = next(gfp)
    #         print(output)
    #         print("\n\n")
    #     except StopIteration:
    #         break

    # pnr = a.insert_booking_details(1)
    # print(pnr)

    # a = AmadeusFlight(originLocation="Mumbai", destinationLocation="Sydney",
    #                   departureDate="2020-07-01", nonStop="false", adults=1, max=5)
    # gfp_ = iter(a.generate_flight_quotes())
    #
    # for output in gfp_:
    #     print(output)
    #     print("\n")

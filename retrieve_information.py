from sqlalchemy import create_engine, MetaData, Table, insert, select
import mysql.connector
from datetime import datetime
import json
from iata_mapping import get_city_name, get_airline_name

currency_code_mapping = {"USD": ["US Dollars","$"], "EUR": ["Euros","€"], "JPY": ["Japanese Yen","¥"], "GBP": ["Pound Sterling","£"], "CHF": ["Swiss Francs","₣"],
                         "INR": ["Indian Rupees","₹"], "AUD": ["Australian Dollars","Aus$"], "CAD": ["Canadian Dollars","Can$"], "CNY": ["Chinese Yuan Renminbi","￥"]}

class RetrieveBookingInformation:
    def __init__(self,pnr):
        self.pnr = pnr
        self.engine = create_engine("mysql+mysqlconnector://root:Trivi@01@127.0.0.1:3306/flightinfodb", encoding="utf-8", echo = False)
        metadata = MetaData()
        self.bookings = Table("bookings",metadata,autoload=True,autoload_with=self.engine)

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

    def passengers_details_format(self, adult_paxno, child_paxno, infant_paxno):
        passenger_details = "{} adults".format(adult_paxno)
        if child_paxno:
            if child_paxno == 1:
                passenger_details += ", 1 child"
            else:
                passenger_details += ", {} children".format(child_paxno)
        if child_paxno:
            if child_paxno == 1:
                passenger_details += ", 1 infant "
            else:
                passenger_details += ", {} infants ".format(infant_paxno)
        return passenger_details

    def terminal_format(self,terminal):
        if terminal:
            return "(Terminal: {})".format(terminal)
        else:
            return ""

    def date_format(self,date):
        return date.strftime("%B %d, %Y").lstrip("0").replace(" 0", " ")

    def time_format(self,time):
        return time.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

    def get_booking_details(self):
        with self.engine.connect() as connection:
            query = select([self.bookings]).where(self.bookings.c.pnr.like(self.pnr + '__%'))
            # query = select([self.bookings]).where(self.bookings.columns.pnr == self.pnr)
            results = connection.execute(query).fetchall()

            if len(results) == 0 or len(self.pnr)<7:
                out = "Sorry no bookings with booking reference {} available".format(self.pnr)
                title = user_name = email_id = country_code = mobile_no = None

            elif len(results) ==  1:
                [pnr, title, user_name, booking_date, source_iata, source_terminal, destination_iata, destination_terminal, depart_date, depart_time, arrive_date, arrive_time, stops, flight_duration, no_of_stops, flight_number,
                adult_paxno, child_paxno, infant_paxno, travel_class, currency, airline_iata, aircraft_type, baggage_allowance_weight, baggage_allowance_unit, email_id, country_code, mobile_no, no_of_checkbags, fare_basis_code,
                base_fare, supplier, ticketing_fee, form_of_payment_fee, tax, grand_total, travel_bound] = results[0]
                stops = json.loads(stops)
                stops_str = self.stops_format(stops["segments"])
                source_terminal = self.terminal_format(source_terminal)
                destination_terminal = self.terminal_format(destination_terminal)
                outbound_params = ["Outbound", get_airline_name(airline_iata), get_city_name(source_iata), source_terminal, self.date_format(depart_date),
                                       self.time_format(depart_time), get_city_name(destination_iata), destination_terminal, self.date_format(arrive_date), self.time_format(arrive_time), " Total duration: "+flight_duration, stops_str]

                passenger_details = self.passengers_details_format(adult_paxno,child_paxno, infant_paxno)
                out += "Welcome back {}. {}. Your booking reference is {}. You booked your flight on {}. Total fare paid: {}. Fare basis code: {}. Baggage allowance: {}. Your email address is {} and mobile number is {}. No of passengers travelling: {}.\n\n".format(title, user_name.strip(), pnr[:-2],get_airline_name(airline_iata),currency_code_mapping.get(currency)[1]+str(grand_total),fare_basis_code,str(baggage_allowance_weight)+baggage_allowance_unit, email_id, "+"+str(country_code)+str(mobile_no), passenger_details)
                out += "{} {} Departure from {}{} on {} at {} --->  Arrival in {}{} on {} at {}. {}. {}\n".format("Outbound: ",*outbound_params)

            else:
                out = ""
                [pnr, title, user_name, booking_date, source_iata, source_terminal, destination_iata, destination_terminal, depart_date, depart_time, arrive_date, arrive_time, stops, flight_duration, no_of_stops, flight_number,
                adult_paxno, child_paxno, infant_paxno, travel_class, currency, airline_iata, aircraft_type, baggage_allowance_weight, baggage_allowance_unit, email_id, country_code, mobile_no, no_of_checkbags, fare_basis_code,
                base_fare, supplier, ticketing_fee, form_of_payment_fee, tax, grand_total, travel_bound] = results[0]
                stops = json.loads(stops)
                stops_str = self.stops_format(stops["segments"])
                source_terminal = self.terminal_format(source_terminal)
                destination_terminal = self.terminal_format(destination_terminal)
                inbound_params = [flight_number,get_city_name(source_iata), source_terminal, self.date_format(depart_date),
                                 self.time_format(depart_time), get_city_name(destination_iata), destination_terminal, self.date_format(arrive_date), self.time_format(arrive_time), " Total duration: "+flight_duration, stops_str]

                [pnr, title, user_name, booking_date, source_iata, source_terminal, destination_iata, destination_terminal, depart_date, depart_time, arrive_date, arrive_time, stops, flight_duration, no_of_stops, flight_number,
                adult_paxno, child_paxno, infant_paxno, travel_class, currency, airline_iata, aircraft_type, baggage_allowance_weight, baggage_allowance_unit, email_id, country_code, mobile_no, no_of_checkbags, fare_basis_code,
                base_fare, supplier, ticketing_fee, form_of_payment_fee, tax, grand_total, travel_bound] = results[1]
                stops = json.loads(stops)
                stops_str = self.stops_format(stops["segments"])
                source_terminal = self.terminal_format(source_terminal)
                destination_terminal = self.terminal_format(destination_terminal)
                outbound_params = [flight_number,get_city_name(source_iata), source_terminal, self.date_format(depart_date),
                                 self.time_format(depart_time), get_city_name(destination_iata), destination_terminal, self.date_format(arrive_date), self.time_format(arrive_time), " Total duration: "+flight_duration, stops_str]

                passenger_details = self.passengers_details_format(adult_paxno,child_paxno, infant_paxno)

                out += "Welcome back {}. {}. Your booking reference is {}. You booked your flight on {}. Total fare paid: {}. Fare basis code: {}. Baggage allowance: {}. Your email address is {} and mobile number is {}. No of passengers travelling: {}.\n\n".format(title, user_name.strip(), pnr[:-2],get_airline_name(airline_iata),currency_code_mapping.get(currency)[1]+str(grand_total),fare_basis_code,str(baggage_allowance_weight)+baggage_allowance_unit, email_id, "+"+str(country_code)+str(mobile_no), passenger_details)
                out += "{} Flight {}. Departure from {}{} on {} at {} --->  Arrival in {}{} on {} at {}. {}. {}\n".format("Outbound: ",*outbound_params)
                out += "{} Flight {}. Departure from {}{} on {} at {} --->  Arrival in {}{} on {} at {}. {}. {}".format("Inbound: ",*inbound_params)

            return out, title, user_name, email_id, country_code, mobile_no

# if __name__ == "__main__":
#     r = RetrieveBookingInformation('PNR5a7d')
#     out, title, user_name, email_id, country_code, mobile_no = r.get_booking_details()
#     print(out)

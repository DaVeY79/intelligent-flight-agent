import pandas as pd
from fuzzywuzzy import process

cityiata_df = pd.read_csv("/Users/davidabraham/Desktop/CityIATA.csv")
airlineiata_df = pd.read_csv("/Users/davidabraham/Desktop/Airline.csv",error_bad_lines=False)

def get_city_iata(city_name):
    cities = list(cityiata_df.City.values)
    closest_city = process.extractOne(city_name,cities)[0]
    city_iata_code = cityiata_df[cityiata_df["City"] == closest_city]["IATA"].values[0]
    return city_iata_code

def get_city_name(city_iata_code):
    cities_iata = list(cityiata_df.IATA.values)
    closest_city_iata = process.extractOne(city_iata_code,cities_iata)[0]
    city_name = cityiata_df[cityiata_df["IATA"] == closest_city_iata]["City"].values[0]
    return city_name

def get_airport_city(airport_name):
    airports = list(cityiata_df.Name.values)
    closest_airport = process.extractOne(airport_name,airports)[0]
    city_name = cityiata_df[cityiata_df["Name"] == closest_airport]["City"].values[0]
    return city_name

def get_airline_iata(airline_name):
    airlines = list(airlineiata_df.Name.values)
    closest_airline = process.extractOne(airline_name,airlines)[0]
    airline_iata_code = airlineiata_df[airlineiata_df["Name"] == closest_airline]["IATA"]
    return airline_iata_code

def get_airline_name(airline_iata_code):
    airlines_iata = list(airlineiata_df.IATA.values)
    closest_airline_iata = process.extractOne(airline_iata_code,airlines_iata)[0]
    airline_name = airlineiata_df[airlineiata_df["IATA"] == closest_airline_iata]["Name"].values[0]
    return airline_name

def get_city_iatas(city_name):
    cities = list(cityiata_df.City.values)
    closest_cities = [closest_city[0] for closest_city in process.extractBests(city_name,cities,limit=5,score_cutoff=80)]
    city_airport_names = cityiata_df[cityiata_df["City"].isin(closest_cities)]["Name"].values[:6]
    city_iata_codes = cityiata_df[cityiata_df["City"].isin(closest_cities)]["IATA"].values[:6]
    return zip(city_airport_names,closest_cities,city_iata_codes)

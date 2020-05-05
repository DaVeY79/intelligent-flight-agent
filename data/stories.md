## say hello
* greet
  - utter_greet

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## flight prices search and ask user for affirmation
* flight
  - flight_booking_form
  - form{"name":"flight_booking_form"}
  - slot{"requested_slot":"fromloc.city_name"}
  - slot{"requested_slot":"toloc.city_name"}
  - slot{"requested_slot":"time"}
  - slot{"requested_slot":"no_of_adults"}
  - slot{"requested_slot":"child_passengers"}
  - slot{"requested_slot":"no_of_children"}
  - slot{"requested_slot":"infant_passengers"}
  - slot{"requested_slot":"no_of_infants"}
  - slot{"requested_slot":"class_type"}
  - slot{"requested_slot":"currency_code"}
  - form{"name":null}
  - slot{"requested_slot": null}
* quote
  - utter_booking
>check_price_search


## flight booking confirmed
>check_price_search
* affirm
  - utter_confirm
  - action_slot_reset
  - utter_goodbye

## flight booking cancelled
>check_price_search
* deny
  - utter_cancellation
  - action_slot_reset
  - utter_goodbye

# flight+airfare information
* flight+airfare
  - utter_flight+airfare
  - utter_acknowledge_help
>check_info_helpful

## user accepts information is helpful direct
>check_info_helpful
* affirm
  - utter_happy
  - utter_goodbye

## user denies information is helpful direct
>check_info_helpful
* deny
  - utter_unhappy
  - utter_goodbye

<!--
## user checks flight time
* flight_time
  - action_flight_time
  - utter_acknowledge_help
>check_timing_info_helpful

## user accepts timing information is helpful
>check_timing_info_helpful
* affirm
  - utter_happy
  - utter_goodbye

## user denies timing information is helpful
>check_timing_info_helpful
* deny
  - utter_unhappy
  - utter_goodbye -->

<!-- ## flight time query
* flight_time
  - utter_flight_time

## utter_airfare
* airfare
  - utter_airfare

## flight query
* flight
  - utter_flight

## flight time query
* flight_time
  - utter_flight_time

## utter_airfare
* airfare
  - utter_airfare -->

<!-- ## interactive_story_1
* greet
    - utter_greet
* flight{"toloc.city_name": "Delhi"}
    - slot{"toloc.city_name": "Delhi"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"toloc.city_name": "Delhi"}
    - slot{"requested_slot": "fromloc.city_name"}
* form: inform_departure_city{"fromloc.city_name": "Pune"}
    - slot{"fromloc.city_name": "Pune"}
    - form: flight_booking_form
    - slot{"fromloc.city_name": "Pune"}
    - slot{"requested_slot": "time"}
* form: inform_departure_date{"time": "2020-09-21T00:00:00.000+00:00", "depart_date.month_name": "September"}
    - slot{"time": "2020-09-21T00:00:00.000+00:00"}
    - form: flight_booking_form
    - slot{"time": "2020-09-21T00:00:00.000+00:00"}
    - form{"name": null}
    - slot{"requested_slot": null}
* affirm
    - action_end_flight_search
    - utter_booking
* affirm
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye
* goodbye
    - utter_goodbye

## interactive_story_2
* greet
    - utter_greet
* flight{"toloc.city_name": "Chennai", "depart_date.day_number": "12th", "depart_date.month_name": "August", "time": "2020-08-12T00:00:00.000+00:00"}
    - slot{"time": "2020-08-12T00:00:00.000+00:00"}
    - slot{"toloc.city_name": "Chennai"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"toloc.city_name": "Chennai"}
    - slot{"time": "2020-08-12T00:00:00.000+00:00"}
    - slot{"requested_slot": "fromloc.city_name"}
* form: inform_departure_city{"fromloc.city_name": "Mumbai"}
    - slot{"fromloc.city_name": "Mumbai"}
    - form: flight_booking_form
    - slot{"fromloc.city_name": "Mumbai"}
    - form{"name": null}
    - slot{"requested_slot": null}
* affirm
    - utter_booking
* affirm
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye

## interactive_story_3
* greet
    - utter_greet
* flight{"fromloc.city_name": "Paris"}
    - slot{"fromloc.city_name": "Paris"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"fromloc.city_name": "Paris"}
    - slot{"requested_slot": "toloc.city_name"}
* flight{"toloc.city_name": "London", "toloc.country_name": "UK"}
    - slot{"toloc.city_name": "London"}
    - utter_ask_time
    - action_listen
* form: inform_departure_date{"depart_date.date_relative": "next", "depart_date.day_name": "wednesday", "time": "2020-04-29T00:00:00.000+00:00"}
    - slot{"time": "2020-04-29T00:00:00.000+00:00"}
    - form{"name": null}
    - slot{"requested_slot": null}
* affirm
    - utter_booking
* affirm
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye
* goodbye
    - utter_goodbye-->

## interactive_story_4
* greet
    - utter_greet
    - action_listen
* flight{"fromloc.city_name": "Amsterdam","toloc.city_name": "Leeds", "depart_date.day_number": "seventh", "depart_date.month_name": "july", "time": "2020-08-12T00:00:00.000+00:00", "depart_date": "2020-08-12T00:00:00.000+00:00"}
    - slot{"fromloc.city_name": "Amsterdam"}
    - slot{"depart_date": "2020-08-12T00:00:00.000+00:00"}
    - slot{"toloc.city_name": "Leeds"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"fromloc.city_name": "Amsterdam"}
    - slot{"depart_date": "2020-08-12T00:00:00.000+00:00"}
    - slot{"toloc.city_name": "Leeds"}
    - slot{"requested_slot": "no_of_adults"}
    - utter_ask_no_of_adults
    - action_listen
* form: inform_no_of_adults{"no_of_adults": "3"}
    - slot{"no_of_adults":"3"}
    - slot{"requested_slot": "child_passengers"}
    - utter_ask_child_passengers
    - action_listen
* affirm
    - slot{"child_passengers": true}
    - slot{"requested_slot": "infant_passengers"}
    - utter_ask_infant_passengers
    - action_listen
* affirm
    - slot{"infant_passengers": true}
    - slot{"requested_slot": "no_of_children"}
    - utter_ask_no_of_children
    - action_listen
* form: inform_no_of_children{"no_of_children": "3"}
    - slot{"no_of_children": "3"}
    - slot{"requested_slot": "no_of_infants"}
    - utter_ask_no_of_infants
    - action_listen
* form: inform_no_of_infants{"no_of_infants": "2"}
    - slot{"no_of_infants": "2"}
    - slot{"requested_slot": "class_type"}
    - utter_ask_class_type
    - action_listen
* form: inform_class_type{"class_type": "PREMIUM_ECONOMY"}
    - slot{"class_type": "PREMIUM_ECONOMY"}
    - slot{"requested_slot": "currency_code"}
    - utter_ask_currency_code
    - action_listen
* form: inform_currency_code{"currency_code": "EUR"}
    - slot{"currency_code": "EUR"}
    - form: flight_booking_form
    - slot{"requested_slot": "round_trip"}
    - utter_ask_round_trip
    - action_listen
* form: inform_round_trip{"round_trip": "round trip"}
    - slot{"round_trip":"round trip"}
    - form: flight_booking_form
    - slot{"requested_slot": "return_date"}
    - utter_ask_return_date
    - action_listen
* form: inform_return_date{"time": "2020-12-30T00:00:00.000+00:00"}
    - slot{"time":"2020-12-30T00:00:00.000+00:00"}
    - form: flight_booking_form
    - slot{"return_date":"2020-12-30T00:00:00.000+00:00"}
    - form: flight_booking_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - flight_booking_form
    - form: flight_booking_form
    - slot{"fromloc.city_name": "Amsterdam"}
    - slot{"depart_date": "2020-08-12T00:00:00.000+00:00"}
    - slot{"toloc.city_name": "Leeds"}
    - slot{"no_of_adults":"3"}
    - slot{"child_passengers": true}
    - slot{"infant_passengers": true}
    - slot{"no_of_children": "3"}
    - slot{"no_of_infants": "2"}
    - slot{"class_type": "PREMIUM_ECONOMY"}
    - slot{"currency_code": "EUR"}
    - slot{"round_trip":"round trip"}
    - slot{"return_date":"2020-12-30T00:00:00.000+00:00"}
    - form{"name": null}
    - slot{"requested_slot": null}
* quote{"quote_id": "4", "number": "4"}
    - slot{"quote_id": "4"}
    - utter_booking
* affirm
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye


## interactive_story_5
* greet
    - utter_greet
    - action_listen
* flight{"fromloc.city_name": "Hong Kong", "toloc.city_name": "Madrid", "depart_date.date_relative": "next", "depart_date.day_name": "thursday", "time": "2020-05-07T00:00:00.000+00:00","depart_date": "2020-05-07T00:00:00.000+00:00"}
    - slot{"fromloc.city_name": "Hong Kong"}
    - slot{"depart_date": "2020-05-07T00:00:00.000+00:00"}
    - slot{"toloc.city_name": "Madrid"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"fromloc.city_name": "Hong Kong"}
    - slot{"toloc.city_name": "Madrid"}
    - slot{"depart_date": "2020-05-07T00:00:00.000+00:00"}
    - slot{"requested_slot": "no_of_adults"}
    - utter_ask_no_of_adults
    - action_listen
* form: inform_no_of_adults{"no_of_adults": "3", "number": 3}
    - slot{"no_of_adults": "3"}
    - form: flight_booking_form
    - slot{"no_of_adults": "3"}
    - slot{"requested_slot": "child_passengers"}
    - utter_ask_child_passengers
    - action_listen
* form: affirm
    - slot{"child_passengers": true}
    - form: flight_booking_form
    - slot{"child_passengers": true}
    - slot{"requested_slot": "infant_passengers"}
    - utter_ask_infant_passengers
    - action_listen
* form: affirm
    - slot{"infant_passengers": true}
    - form: flight_booking_form
    - slot{"infant_passengers": true}
    - slot{"requested_slot": "no_of_children"}
    - utter_ask_no_of_children
    - action_listen
* form: inform_no_of_children{"no_of_children": "3", "number": 3}
    - slot{"no_of_children": "3"}
    - form: flight_booking_form
    - slot{"no_of_children": "3"}
    - slot{"requested_slot": "no_of_infants"}
    - utter_ask_no_of_infants
    - action_listen
* form: inform_no_of_infants{"no_of_infants": "2", "number": 2}
    - slot{"no_of_infants": "2"}
    - form: flight_booking_form
    - slot{"requested_slot": "class_type"}
    - utter_ask_class_type
    - action_listen
* form: inform_class_type{"class_type": "BUSINESS"}
    - slot{"class_type": "BUSINESS"}
    - form: flight_booking_form
    - slot{"requested_slot": "currency_code"}
    - utter_ask_currency_code
    - action_listen
* form: inform_currency_code{"currency_code": "USD"}
    - slot{"currency_code": "USD"}
    - form: flight_booking_form
    - slot{"requested_slot": "round_trip"}
    - utter_ask_round_trip
    - action_listen
* form: inform_round_trip{"round_trip": "round trip"}
    - slot{"round_trip":"round trip"}
    - form: flight_booking_form
    - slot{"requested_slot": "return_date"}
    - utter_ask_return_date
    - action_listen
* form: inform_round_trip{"time": "2020-07-07T00:00:00.000+00:00"}
    - slot{"time":"2020-07-07T00:00:00.000+00:00"}
    - form: flight_booking_form
    - slot{"return_date":"2020-07-07T00:00:00.000+00:00"}
    - form: flight_booking_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - flight_booking_form
    - form: flight_booking_form
    - slot{"fromloc.city_name": "Hong Kong"}
    - slot{"toloc.city_name": "Madrid"}
    - slot{"depart_date": "2020-05-07T00:00:00.000+00:00"}
    - slot{"no_of_adults": "3"}
    - slot{"child_passengers": true}
    - slot{"infant_passengers": true}
    - slot{"no_of_children": "3"}
    - slot{"no_of_infants": "2"}
    - slot{"class_type": "BUSINESS"}
    - slot{"currency_code": "USD"}
    - slot{"round_trip":"round trip"}
    - slot{"return_date":"2020-07-07T00:00:00.000+00:00"}
    - form{"name": null}
    - slot{"requested_slot": null}
* quote{"quote_id": "2", "number": "2"}
    - slot{"quote_id": "2"}
    - utter_booking
* affirm
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye

## interactive_story_6
* greet
    - utter_greet
    - action_listen
* flight{"toloc.city_name": "Dubai", "time": "2020-10-05T00:00:00.000+00:00", "depart_date.month_name": "October", "depart_date.day_number": "5th"}
    - slot{"time": "2020-10-05T00:00:00.000+00:00"}
    - slot{"toloc.city_name": "Dubai"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"toloc.city_name": "Dubai"}
    - slot{"time": "2020-10-05T00:00:00.000+00:00"}
    - slot{"toloc.city_name": "Dubai"}
    - slot{"time": "2020-10-05T00:00:00.000+00:00"}
    - slot{"requested_slot": "fromloc.city_name"}
* form: flight{"fromloc.city_name": "Bangalore"}
    - slot{"fromloc.city_name": "Bangalore"}
    - form: flight_booking_form
    - slot{"requested_slot": "no_of_adults"}
    - utter_ask_no_of_adults
    - action_listen
* form: inform_no_of_adults{"no_of_adults": "3", "number": 3}
    - slot{"no_of_adults": "3"}
    - form: flight_booking_form
    - slot{"requested_slot": "child_passengers"}
    - utter_ask_child_passengers
    - action_listen
* form: affirm
    - slot{"child_passengers": true}
    - form: flight_booking_form
    - slot{"requested_slot": "infant_passengers"}
    - utter_ask_infant_passengers
    - action_listen
* form: affirm
    - slot{"infant_passengers": true}
    - form: flight_booking_form
    - slot{"requested_slot": "no_of_children"}
    - utter_ask_no_of_children
    - action_listen
* form: inform_no_of_children{"no_of_children": "3", "number": 3}
    - slot{"no_of_children": "3"}
    - form: flight_booking_form
    - slot{"requested_slot": "no_of_infants"}
    - utter_ask_no_of_infants
    - action_listen
* form: inform_no_of_infants{"no_of_infants": "1", "number": 1}
    - slot{"no_of_infants": "1"}
    - form: flight_booking_form
    - slot{"requested_slot": "class_type"}
    - utter_ask_class_type
    - action_listen
* form: inform_class_type{"class_type": "ECONOMY"}
    - slot{"class_type": "ECONOMY"}
    - flight_booking_form
    - slot{"requested_slot": "currency_code"}
    - utter_ask_currency_code
    - action_listen
* form: inform_currency_code{"currency_code": "INR"}
    - slot{"currency_code": "INR"}
    - flight_booking_form
    - slot{"requested_slot": "round_trip"}
    - utter_ask_round_trip
    - action_listen
* form: inform_round_trip{"round_trip": "one way"}
    - slot{"round_trip":"one way"}
    - flight_booking_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"fromloc.city_name": "Bangalore"}
    - slot{"toloc.city_name": "Dubai"}
    - slot{"time": "2020-10-05T00:00:00.000+00:00"}
    - slot{"no_of_adults": "3"}
    - slot{"child_passengers": true}
    - slot{"infant_passengers": true}
    - slot{"no_of_children": "3"}
    - slot{"no_of_infants": "1"}
    - slot{"class_type": "ECONOMY"}
    - slot{"currency_code": "INR"}
    - form{"name": null}
    - slot{"requested_slot": null}
* quote{"quote_id": "5", "number": "5"}
    - slot{"quote_id": "5"}
    - utter_booking
* affirm
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye

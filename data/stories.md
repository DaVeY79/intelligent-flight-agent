## say hello
* greet
  - utter_greet

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## user provide pnr
* inform_pnr
  - utter_wait_pnr
  - retrieve_booking_info_form
  - form{"name":"retrieve_booking_info_form"}
  - form{"name":null}
  - slot{"requested_slot": null}
  - utter_other_help


## ask user for departure, arrival city and no of adults travelling
* flight OR flight+airfare
  - flight_booking_form
  - form{"name":"flight_booking_form"}
  - slot{"requested_slot":"fromloc.city_name"}
  - utter_ask_fromloc.city_name
  - action_listen
* form: inform_departure_city
  - form: flight_booking_form
  - slot{"requested_slot":"toloc.city_name"}
  - utter_ask_toloc.city_name
  - action_listen
* form: inform_arrival_city
  - form: flight_booking_form
  - slot{"requested_slot":"depart_date"}
  - utter_ask_depart_date
  - action_listen
* form: inform_arrival_city
  - form: flight_booking_form
  - slot{"requested_slot":"no_of_adults"}
  - utter_ask_no_of_adults
  - action_listen
* form: inform_no_of_adults
>check_basic_details

## user affirms children travelling
>check_basic_details
  - form: flight_booking_form
  - slot{"requested_slot":"child_passengers"}
  - utter_ask_child_passengers
  - action_listen
* form: affirm
  - slot{"child_passengers": true}
  - form: flight_booking_form
  - slot{"requested_slot":"no_of_children"}
  - utter_ask_no_of_children
  - action_listen
* form: inform_no_of_children
>check_child_passengers_affirm

## user denies children travelling
>check_basic_details
  - form: flight_booking_form
  - slot{"requested_slot":"child_passengers"}
  - utter_ask_child_passengers
  - action_listen
* form: deny
  - slot{"child_passengers": false}
>check_child_passengers_deny

## user affirms infants travelling
>check_child_passengers_affirm
>check_child_passengers_deny
  - form: flight_booking_form
  - slot{"requested_slot":"infant_passengers"}
  - utter_ask_infant_passengers
  - action_listen
* form: affirm
  - slot{"infant_passengers": true}
  - form: flight_booking_form
  - slot{"requested_slot":"no_of_infants"}
  - utter_ask_no_of_infants
  - action_listen
* form: inform_no_of_infants
>check_infant_passengers_affirm

## user denies infants travelling
>check_child_passengers_affirm
>check_child_passengers_deny
  - form: flight_booking_form
  - slot{"requested_slot":"infant_passengers"}
  - utter_ask_infant_passengers
  - action_listen
* form: deny
  - slot{"infant_passengers": false}
>check_infant_passengers_deny

## flight asks for travel class and payment currency
>check_infant_passengers_affirm
>check_infant_passengers_deny
  - form: flight_booking_form
  - slot{"requested_slot":"class_type"}
  - utter_ask_class_type
  - action_listen
* form: inform_class_type
  - form: flight_booking_form
  - slot{"requested_slot":"currency_code"}
  - utter_ask_currency_code
  - action_listen
* form: inform_currency_code
>check_class_currency

## user asks for round trip
>check_class_currency
  - form: flight_booking_form
  - slot{"requested_slot":"round_trip"}
  - utter_ask_round_trip
  - action_listen
* form: inform_round_trip{"round_trip": "round trip"}
  - slot{"round_trip":"round trip"}
  - form: flight_booking_form
  - slot{"requested_slot": "return_date"}
  - utter_ask_return_date
  - action_listen
* form: inform_return_date
>check_round_trip


## user asks for one way
>check_class_currency
  - form: flight_booking_form
  - slot{"requested_slot":"round_trip"}
  - utter_ask_round_trip
  - action_listen
* form: inform_round_trip{"round_trip": "one way"}
  - slot{"round_trip":"one way"}
>check_one_way

## users asks for direct flight
>check_round_trip
>check_one_way
  - form: flight_booking_form
  - slot{"requested_slot":"flight_stop_check"}
  - utter_ask_flight_stop_check
  - action_listen
* form: inform_flight_stop_check{"flight_stop_check"="true"}
>check_direct_flight

## users asks for connecting flight
>check_round_trip
>check_one_way
  - form: flight_booking_form
  - slot{"requested_slot":"flight_stop_check"}
  - utter_ask_flight_stop_check
  - action_listen
* form: inform_flight_stop_check{"flight_stop_check"="false"}
>check_indirect_flight


## user details
>check_direct_flight
>check_indirect_flight
  - form: flight_booking_form
  - slot{"requested_slot":"email_id"}
  - utter_ask_email_id
  - action_listen
* form: inform_email_id
  - form: flight_booking_form
  - slot{"requested_slot":"title"}
  - utter_ask_title
  - action_listen
* form: inform_title
  - form: flight_booking_form
  - slot{"requested_slot":"user_name"}
  - utter_ask_user_name
  - action_listen
* form: inform_user_name
  - form: flight_booking_form
  - slot{"requested_slot":"mobile_no"}
  - utter_ask_mobile_no
  - action_listen
* form: inform_mobile_no
  - form: flight_booking_form
  - slot{"requested_slot":"country_code"}
  - utter_ask_country_code
  - action_listen
* form: inform_country_code
>get_user_details

## flight prices search and ask user for affirmation
>get_user_details
  - form{"name":null}
  - slot{"requested_slot": null}
* quote
  - utter_booking
>check_price_search


## flight booking confirmed
>check_price_search
* affirm
  - action_booking_confirmation
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
    - utter_goodbye-->

## interactive_story_2
* greet
    - utter_greet
* flight{"toloc.city_name": "Chennai", "depart_date.day_number": "12th", "depart_date.month_name": "August", "time": "2020-08-12T00:00:00.000+00:00"}
    - slot{"time": "2020-08-12T00:00:00.000+00:00"}
    - slot{"depart_date": "2020-08-12"}
    - slot{"toloc.city_name": "Chennai"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"requested_slot": "fromloc.city_name"}
    - utter_ask_fromloc.city_name
    - action_listen
* form: inform_departure_city{"fromloc.city_name": "Mumbai"}
    - slot{"fromloc.city_name": "Mumbai"}
    - form: flight_booking_form
    - slot{"fromloc.city_name": "Mumbai"}
    - slot{"requested_slot": "no_of_adults"}
    - utter_ask_no_of_adults
    - action_listen
* form: inform_no_of_adults{"no_of_adults": "1"}
    - slot{"no_of_adults":"1"}
    - form: flight_booking_form
    - slot{"requested_slot": "child_passengers"}
    - utter_ask_child_passengers
    - action_listen
* deny
    - slot{"child_passengers": false}
    - form: flight_booking_form
    - slot{"requested_slot": "infant_passengers"}
    - utter_ask_infant_passengers
    - action_listen
* deny
    - slot{"infant_passengers": false}
    - form: flight_booking_form
    - slot{"requested_slot": "class_type"}
    - utter_ask_class_type
    - action_listen
* form: inform_class_type{"class_type": "ECONOMY"}
    - slot{"class_type": "ECONOMY"}
    - form: flight_booking_form
    - slot{"requested_slot": "currency_code"}
    - utter_ask_currency_code
    - action_listen
* form: inform_currency_code{"currency_code": "INR"}
    - slot{"currency_code": "INR"}
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
* form: inform_return_date{"return_date.day_number":"thirtieth","return_date.month_name":"August","time": "2020-08-30T00:00:00.000+00:00"}
    - slot{"time":"2020-08-30T00:00:00.000+00:00"}
    - slot{"return_date":"2020-08-30"}
    - form: flight_booking_form
    - slot{"requested_slot": "flight_stop_check"}
    - utter_ask_flight_stop_check
    - action_listen
* form: deny
    - slot{"flight_stop_check":"false"}
    - form: flight_booking_form
    - slot{"requested_slot":"email_id"}
    - utter_ask_email_id
    - action_listen
* form: inform_email_id{"email_id":"pranav.sethi@gmail.com"}
    - slot{"email_id":"pranav.sethi@gmail.com"}
    - form: flight_booking_form
    - slot{"requested_slot":"title"}
    - utter_ask_title
    - action_listen
* form: inform_title{"title":"Mr"}
    - slot{"title":"Mr"}
    - form: flight_booking_form
    - slot{"requested_slot":"user_name"}
    - utter_ask_user_name
    - action_listen
* form: inform_user_name{"user_name":"Pranav Sethi"}
    - slot{"user_name":"Pranav Sethi"}
    - form: flight_booking_form
    - slot{"requested_slot":"mobile_no"}
    - utter_ask_mobile_no
    - action_listen
* form: inform_mobile_no{"mobile_no":"8750345990"}
    - slot{"mobile_no":"8750345990"}
    - form: flight_booking_form
    - slot{"requested_slot":"country_code"}
    - utter_ask_country_code
    - action_listen
* form: inform_country_code{"country_code":"91"}   
    - slot{"country_code":"91"}
    - form: flight_booking_form
    - slot{"fromloc.city_name": "Mumbai"}
    - slot{"toloc.city_name": "Chennai"}
    - slot{"depart_date": "2020-08-12"}
    - slot{"no_of_adults":"1"}
    - slot{"child_passengers": false}
    - slot{"infant_passengers": false}
    - slot{"no_of_children": "0"}
    - slot{"no_of_infants": "0"}
    - slot{"class_type": "ECONOMY"}
    - slot{"currency_code": "INR"}
    - slot{"round_trip":"round trip"}
    - slot{"return_date":"2020-08-30"}
    - slot{"email_id":"pranav.sethi@gmail.com"}
    - slot{"title":"Mr"}
    - slot{"user_name":"Pranav Sethi"}
    - slot{"mobile_no":"8750345990"}
    - slot{"country_code":"91"}
    - form{"name": null}
    - slot{"requested_slot": null}
* quote{"quote_id": "7", "number": "7"}
    - slot{"quote_id": "7"}
    - utter_booking
* affirm
    - action_booking_confirmation
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
    - utter_ask_toloc.city_name
    - action_listen
* form: inform_departure_city{"toloc.city_name": "London", "toloc.country_name": "UK"}
    - slot{"toloc.city_name": "London"}
    - form: flight_booking_form
    - slot{"requested_slot": "depart_date"}
    - utter_ask_depart_date
    - action_listen
* form: inform_departure_date{"depart_date.date_relative": "next", "depart_date.day_name": "wednesday", "time": "2020-04-29T00:00:00.000+00:00","depart_date": "2020-04-29"}
    - slot{"depart_date": "2020-04-29"}
    - form: flight_booking_form
    - slot{"requested_slot": "no_of_adults"}
    - utter_ask_no_of_adults
    - action_listen
* form: inform_no_of_adults{"no_of_adults": "3"}
    - slot{"no_of_adults":"3"}
    - form: flight_booking_form
    - slot{"requested_slot": "child_passengers"}
    - utter_ask_child_passengers
    - action_listen
* deny
    - slot{"child_passengers": false}
    - form: flight_booking_form
    - slot{"requested_slot": "infant_passengers"}
    - utter_ask_infant_passengers
    - action_listen
* affirm
    - slot{"infant_passengers": true}
    - form: flight_booking_form
    - slot{"requested_slot": "no_of_infants"}
    - utter_ask_no_of_infants
    - action_listen
* form: inform_no_of_infants{"no_of_infants": "1"}
    - slot{"no_of_infants": "1"}
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
* form: inform_currency_code{"currency_code": "EUR"}
    - slot{"currency_code": "EUR"}
    - form: flight_booking_form
    - slot{"requested_slot": "round_trip"}
    - utter_ask_round_trip
    - action_listen
* form: inform_round_trip{"round_trip": "one way"}
    - slot{"round_trip":"one way"}
    - form: flight_booking_form
    - slot{"requested_slot": "flight_stop_check"}
    - utter_ask_flight_stop_check
    - action_listen
* form: deny
    - slot{"flight_stop_check":"false"}
    - form: flight_booking_form
    - slot{"requested_slot":"email_id"}
    - utter_ask_email_id
    - action_listen
* form: inform_email_id{"email_id":"melinda.pienthiere@lespac.fr"}
    - slot{"email_id":"melinda.pienthiere@lespac.fr"}
    - form: flight_booking_form
    - slot{"requested_slot":"title"}
    - utter_ask_title
    - action_listen
* form: inform_title{"title":"Ms"}
    - slot{"title":"Ms"}
    - form: flight_booking_form
    - slot{"requested_slot":"user_name"}
    - utter_ask_user_name
    - action_listen
* form: inform_user_name{"user_name":"Melinda Pienthiere"}
    - slot{"user_name":"Melinda Pienthiere"}
    - form: flight_booking_form
    - slot{"requested_slot":"mobile_no"}
    - utter_ask_mobile_no
    - action_listen
* form: inform_mobile_no{"mobile_no":"7732345990"}
    - slot{"mobile_no":"7732345990"}
    - form: flight_booking_form
    - slot{"requested_slot":"country_code"}
    - utter_ask_country_code
    - action_listen
* form: inform_country_code{"country_code":"33"}   
    - slot{"country_code":"33"}
    - form: flight_booking_form
    - slot{"fromloc.city_name": "Paris"}
    - slot{"toloc.city_name": "London"}
    - slot{"depart_date": "2020-04-29"}
    - slot{"no_of_adults":"3"}
    - slot{"child_passengers": false}
    - slot{"infant_passengers": true}
    - slot{"no_of_infants": "1"}
    - slot{"class_type": "BUSINESS"}
    - slot{"currency_code": "EUR"}
    - slot{"round_trip":"one way"}
    - slot{"email_id":"melinda.pienthiere@lespac.fr"}
    - slot{"title":"Ms"}
    - slot{"user_name":"Melinda Pienthiere"}
    - slot{"mobile_no":"7732345990"}
    - slot{"country_code":"33"}
    - form{"name": null}
    - slot{"requested_slot": null}
* quote{"quote_id": "3", "number": "3"}
    - slot{"quote_id": "3"}
    - utter_booking
* affirm
    - action_booking_confirmation
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye
* goodbye
    - utter_goodbye

## interactive_story_4
* greet
    - utter_greet
    - action_listen
* flight{"fromloc.city_name": "Amsterdam","toloc.city_name": "Leeds", "depart_date.day_number": "seventh", "depart_date.month_name": "july", "time": "2020-08-12T00:00:00.000+00:00"}
    - slot{"fromloc.city_name": "Amsterdam"}
    - slot{"depart_date": "2020-08-12"}
    - slot{"toloc.city_name": "Leeds"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"requested_slot": "no_of_adults"}
    - utter_ask_no_of_adults
    - action_listen
* form: inform_no_of_adults{"no_of_adults": "3"}
    - slot{"no_of_adults":"3"}
    - form{"name": "flight_booking_form"}
    - slot{"requested_slot": "child_passengers"}
    - utter_ask_child_passengers
    - action_listen
* affirm
    - slot{"child_passengers": true}
    - form{"name": "flight_booking_form"}
    - slot{"requested_slot": "no_of_children"}
    - utter_ask_no_of_children
    - action_listen
* form: inform_no_of_children{"no_of_children": "3"}
    - slot{"no_of_children": "3"}
    - form{"name": "flight_booking_form"}
    - slot{"requested_slot": "infant_passengers"}
    - utter_ask_infant_passengers
    - action_listen
* affirm
    - slot{"infant_passengers": true}
    - form{"name": "flight_booking_form"}
    - slot{"requested_slot": "no_of_infants"}
    - utter_ask_no_of_infants
    - action_listen
* form: inform_no_of_infants{"no_of_infants": "2"}
    - slot{"no_of_infants": "2"}
    - form{"name": "flight_booking_form"}
    - slot{"requested_slot": "class_type"}
    - utter_ask_class_type
    - action_listen
* form: inform_class_type{"class_type": "PREMIUM_ECONOMY"}
    - slot{"class_type": "PREMIUM_ECONOMY"}
    - form{"name": "flight_booking_form"}
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
* form: inform_return_date{"return_date.day_number":"30th","return_date.month_name":"December","time": "2020-12-30T00:00:00.000+00:00"}
    - slot{"time":"2020-12-30T00:00:00.000+00:00"}
    - slot{"return_date":"2020-12-30"}
    - form: flight_booking_form
    - slot{"requested_slot": "flight_stop_check"}
    - utter_ask_flight_stop_check
    - action_listen
* form: affirm
    - slot{"flight_stop_check":"true"}
    - form: flight_booking_form
    - slot{"requested_slot":"email_id"}
    - utter_ask_email_id
    - action_listen
* form: inform_email_id{"email_id":"robin.van.persie@arsenal.epl.com"}
    - slot{"email_id":"robin.van.persie@arsenal.epl.com"}
    - form: flight_booking_form
    - slot{"requested_slot":"title"}
    - utter_ask_title
    - action_listen
* form: inform_title{"title":"Mr"}
    - slot{"title":"Mr"}
    - form: flight_booking_form
    - slot{"requested_slot":"user_name"}
    - utter_ask_user_name
    - action_listen
* form: inform_user_name{"user_name":"Robin Van Persie"}
    - slot{"user_name":"Robin Van Persie"}
    - form: flight_booking_form
    - slot{"requested_slot":"mobile_no"}
    - utter_ask_mobile_no
    - action_listen
* form: inform_mobile_no{"mobile_no":"7777345990"}
    - slot{"mobile_no":"7777345990"}
    - form: flight_booking_form
    - slot{"requested_slot":"country_code"}
    - utter_ask_country_code
    - action_listen
* form: inform_country_code{"country_code":"31"}   
    - slot{"country_code":"31"}
    - form: flight_booking_form
    - slot{"fromloc.city_name": "Amsterdam"}
    - slot{"depart_date": "2020-08-12"}
    - slot{"toloc.city_name": "Leeds"}
    - slot{"no_of_adults":"3"}
    - slot{"child_passengers": true}
    - slot{"infant_passengers": true}
    - slot{"no_of_children": "3"}
    - slot{"no_of_infants": "2"}
    - slot{"class_type": "PREMIUM_ECONOMY"}
    - slot{"currency_code": "EUR"}
    - slot{"round_trip":"round trip"}
    - slot{"return_date":"2020-12-30"}
    - slot{"email_id":"robin.van.persie@arsenal.epl.com"}
    - slot{"title":"Mr"}
    - slot{"user_name":"Robin Van Persie"}
    - slot{"mobile_no":"7777345990"}
    - slot{"country_code":"31"}
    - form{"name": null}
    - slot{"requested_slot": null}
* quote{"quote_id": "4", "number": "4"}
    - slot{"quote_id": "4"}
    - utter_booking
* affirm
    - action_booking_confirmation
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye


## interactive_story_5
* greet
    - utter_greet
    - action_listen
* flight{"fromloc.city_name": "Hong Kong", "toloc.city_name": "Madrid", "depart_date.date_relative": "next", "depart_date.day_name": "thursday", "time": "2020-05-07T00:00:00.000+00:00"}
    - slot{"fromloc.city_name": "Hong Kong"}
    - slot{"time": "2020-05-07T00:00:00.000+00:00"}
    - slot{"toloc.city_name": "Madrid"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"fromloc.city_name": "Hong Kong"}
    - slot{"toloc.city_name": "Madrid"}
    - slot{"depart_date": "2020-05-07"}
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
    - slot{"requested_slot": "no_of_children"}
    - utter_ask_no_of_children
    - action_listen
* form: inform_no_of_children{"no_of_children": "3", "number": 3}
    - slot{"no_of_children": "3"}
    - form: flight_booking_form
    - slot{"requested_slot": "infant_passengers"}
    - utter_ask_infant_passengers
    - action_listen
* form: affirm
    - slot{"infant_passengers": true}
    - form: flight_booking_form
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
    - slot{"return_date":"2020-07-07"}
    - form: flight_booking_form
    - slot{"requested_slot": "flight_stop_check"}
    - utter_ask_flight_stop_check
    - action_listen
* form: deny
    - slot{"flight_stop_check":"false"}
    - form: flight_booking_form
    - slot{"requested_slot":"email_id"}
    - utter_ask_email_id
    - action_listen
* form: inform_email_id{"email_id":"patricia.wu@sinawiebo.ch"}
    - slot{"email_id":"patrick.wu@sinawiebo.ch"}
    - form: flight_booking_form
    - slot{"requested_slot":"title"}
    - utter_ask_title
    - action_listen
* form: inform_title{"title":"Ms"}
    - slot{"title":"Ms"}
    - form: flight_booking_form
    - slot{"requested_slot":"user_name"}
    - utter_ask_user_name
    - action_listen
* form: inform_user_name{"user_name":"Patricia Wu"}
    - slot{"user_name":"Patricia Wu"}
    - form: flight_booking_form
    - slot{"requested_slot":"mobile_no"}
    - utter_ask_mobile_no
    - action_listen
* form: inform_mobile_no{"mobile_no":"8888345990"}
    - slot{"mobile_no":"8888345990"}
    - form: flight_booking_form
    - slot{"requested_slot":"country_code"}
    - utter_ask_country_code
    - action_listen
* form: inform_country_code{"country_code":"852"}   
    - slot{"country_code":"852"}
    - form: flight_booking_form
    - slot{"fromloc.city_name": "Hong Kong"}
    - slot{"toloc.city_name": "Madrid"}
    - slot{"depart_date": "2020-05-07"}
    - slot{"no_of_adults": "3"}
    - slot{"child_passengers": true}
    - slot{"infant_passengers": true}
    - slot{"no_of_children": "3"}
    - slot{"no_of_infants": "2"}
    - slot{"class_type": "BUSINESS"}
    - slot{"currency_code": "USD"}
    - slot{"round_trip":"round trip"}
    - slot{"return_date":"2020-07-07"}
    - slot{"email_id":"patrick.wu@sinawiebo.ch"}
    - slot{"title":"Ms"}
    - slot{"user_name":"Patricia Wu"}
    - slot{"mobile_no":"8888345990"}
    - slot{"country_code":"852"}
    - form{"name": null}
    - slot{"requested_slot": null}
* quote{"quote_id": "2", "number": "2"}
    - slot{"quote_id": "2"}
    - utter_booking
* affirm
    - action_booking_confirmation
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye

## interactive_story_6
* greet
    - utter_greet
    - action_listen
* flight{"toloc.city_name": "Dubai", "time": "2020-10-05T00:00:00.000+00:00", "depart_date.month_name": "October", "depart_date.day_number": "5th","depart_date": "2020-10-05"}
    - slot{"toloc.city_name": "Dubai"}
    - slot{"depart_date": "2020-10-05"}
    - slot{"time": "2020-10-05T00:00:00.000+00:00"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
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
    - slot{"requested_slot": "no_of_children"}
    - utter_ask_no_of_children
    - action_listen
* form: inform_no_of_children{"no_of_children": "3", "number": 3}
    - slot{"no_of_children": "3"}
    - form: flight_booking_form
    - slot{"requested_slot": "infant_passengers"}
    - utter_ask_infant_passengers
    - action_listen
* form: affirm
    - slot{"infant_passengers": true}
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
    - form: flight_booking_form
    - slot{"requested_slot": "currency_code"}
    - utter_ask_currency_code
    - action_listen
* form: inform_currency_code{"currency_code": "INR"}
    - slot{"currency_code": "INR"}
    - form: flight_booking_form
    - slot{"requested_slot": "round_trip"}
    - utter_ask_round_trip
    - action_listen
* form: inform_round_trip{"round_trip": "one way"}
    - slot{"round_trip":"one way"}
    - form: flight_booking_form
    - slot{"requested_slot": "flight_stop_check"}
    - utter_ask_flight_stop_check
    - action_listen
* form: affirm
    - slot{"flight_stop_check":"true"}
    - form: flight_booking_form
    - slot{"requested_slot":"email_id"}
    - utter_ask_email_id
    - action_listen
* form: inform_email_id{"email_id":"abdul.jabbar@emirates.ae"}
    - slot{"email_id":"abdul.jabar@emirates.ae"}
    - form: flight_booking_form
    - slot{"requested_slot":"title"}
    - utter_ask_title
    - action_listen
* form: inform_title{"title":"Mr"}
    - slot{"title":"Mr"}
    - form: flight_booking_form
    - slot{"requested_slot":"user_name"}
    - utter_ask_user_name
    - action_listen
* form: inform_user_name{"user_name":"Abdul Jabbar"}
    - slot{"user_name":"Abdul Jabbar"}
    - form: flight_booking_form
    - slot{"requested_slot":"mobile_no"}
    - utter_ask_mobile_no
    - action_listen
* form: inform_mobile_no{"mobile_no":"8876345990"}
    - slot{"mobile_no":"8876345990"}
    - form: flight_booking_form
    - slot{"requested_slot":"country_code"}
    - utter_ask_country_code
    - action_listen
* form: inform_country_code{"country_code":"971"}   
    - slot{"country_code":"971"}
    - flight_booking_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"fromloc.city_name": "Bangalore"}
    - slot{"toloc.city_name": "Dubai"}
    - slot{"depart_date": "2020-10-05"}
    - slot{"no_of_adults": "3"}
    - slot{"child_passengers": true}
    - slot{"infant_passengers": true}
    - slot{"no_of_children": "3"}
    - slot{"no_of_infants": "1"}
    - slot{"class_type": "ECONOMY"}
    - slot{"currency_code": "INR"}
    - slot{"email_id":"abdul.jabar@emirates.ae"}
    - slot{"title":"Mr"}
    - slot{"user_name":"Abdul Jabbar"}
    - slot{"mobile_no":"8876345990"}
    - slot{"country_code":"971"}
    - form{"name": null}
    - slot{"requested_slot": null}
* quote{"quote_id": "5", "number": "5"}
    - slot{"quote_id": "5"}
    - utter_booking
* affirm
    - action_booking_confirmation
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye

    <!-- insert line 309 - form{"name": null}
    - slot{"requested_slot": null}
    - flight_booking_form
    - form: flight_booking_form -->

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

<!--
## flight time query
* flight_time
  - utter_flight_time

## utter_airfare
* airfare
  - utter_airfare

## flight query
* flight
  - utter_flight

## utter_airfare
* airfare
  - utter_airfare -->

## interactive_story_7
* greet
    - utter_greet
* flight{"fromloc.city_name": "Mumbai", "toloc.city_name": "Sydney", "depart_date.month_name": "august", "depart_date.day_number": "3rd", "time": "2020-08-03T00:00:00.000+00:00"}
    - slot{"fromloc.city_name": "Mumbai"}
    - slot{"time": "2020-08-03T00:00:00.000+00:00"}
    - slot{"toloc.city_name": "Sydney"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"fromloc.city_name": "Mumbai"}
    - slot{"toloc.city_name": "Sydney"}
    - slot{"requested_slot": "depart_date"}
* form: inform_departure_date{"depart_date.month_name": "august", "depart_date.day_number": "3rd", "time": "2020-08-03T00:00:00.000+00:00"}
    - slot{"time": "2020-08-03T00:00:00.000+00:00"}
    - form: flight_booking_form
    - slot{"depart_date": "2020-08-03"}
    - slot{"requested_slot": "no_of_adults"}
* form: inform_no_of_adults{"no_of_adults": "2", "number": 2}
    - slot{"no_of_adults": "2"}
    - form: flight_booking_form
    - slot{"no_of_adults": "2"}
    - slot{"requested_slot": "child_passengers"}
* form: deny
    - form: flight_booking_form
    - slot{"child_passengers": false}
    - slot{"no_of_children": 0}
    - slot{"requested_slot": "infant_passengers"}
* form: affirm
    - form: flight_booking_form
    - slot{"infant_passengers": true}
    - slot{"requested_slot": "class_type"}
    - utter_ask_no_of_infants
* inform_no_of_infants{"no_of_infants": "1", "number": 1}
    - slot{"no_of_infants": "1"}
    - flight_booking_form
    - slot{"requested_slot": "class_type"}
    - utter_ask_class_type
    - action_listen
* form: inform_class_type{"class_type": "ECONOMY"}
    - slot{"class_type": "ECONOMY"}
    - flight_booking_form
    - slot{"class_type": "ECONOMY"}
    - slot{"requested_slot": "currency_code"}
    - utter_ask_currency_code
    - action_listen
* form: inform_currency_code{"currency_code": "USD"}
    - slot{"currency_code": "USD"}
    - flight_booking_form
    - slot{"currency_code": "USD"}
    - slot{"requested_slot": "round_trip"}
    - utter_ask_round_trip
    - action_listen
* form: inform_round_trip{"round_trip": "round trip"}
    - slot{"round_trip": "round trip"}
    - flight_booking_form
    - slot{"round_trip": "round trip"}
    - slot{"requested_slot": "return_date"}
* form: inform_return_date{"round_trip": "round trip", "time": "2020-11-25T00:00:00.000+00:00", "return_date.month_name": "November", "return_date.day_number": "25th", "return_date.year": "2020"}
    - slot{"round_trip": "round trip"}
    - slot{"time": "2020-11-25T00:00:00.000+00:00"}
    - form: flight_booking_form
    - slot{"return_date": "2020-11-25"}
    - slot{"requested_slot": "flight_stop_check"}
* form: affirm
    - slot{"flight_stop_check": "true"}
    - form: flight_booking_form
    - slot{"requested_slot":"email_id"}
    - utter_ask_email_id
    - action_listen
* form: inform_email_id{"email_id":"kareena.kapoor@bollywood.in"}
    - slot{"email_id":"kareena.kapoor@bollywood.in"}
    - form: flight_booking_form
    - slot{"requested_slot":"title"}
    - utter_ask_title
    - action_listen
* form: inform_title{"title":"Ms"}
    - slot{"title":"Ms"}
    - form: flight_booking_form
    - slot{"requested_slot":"user_name"}
    - utter_ask_user_name
    - action_listen
* form: inform_user_name{"user_name":"Kareena Kapoor"}
    - slot{"user_name":"Kareena Kapoor"}
    - form: flight_booking_form
    - slot{"requested_slot":"mobile_no"}
    - utter_ask_mobile_no
    - action_listen
* form: inform_mobile_no{"mobile_no":"8876345750"}
    - slot{"mobile_no":"8876345750"}
    - form: flight_booking_form
    - slot{"requested_slot":"country_code"}
    - utter_ask_country_code
    - action_listen
* form: inform_country_code{"country_code":"91"}   
    - slot{"country_code":"91"}
    - form: flight_booking_form
    - slot{"fromloc.city_name": "Mumbai"}
    - slot{"toloc.city_name": "Sydney"}
    - slot{"depart_date": "2020-08-03"}
    - slot{"no_of_adults": "2"}
    - slot{"child_passengers": false}
    - slot{"infant_passengers": true}
    - slot{"class_type": "ECONOMY"}
    - slot{"no_of_infants": "1"}
    - slot{"currency_code": "USD"}
    - slot{"round_trip": "round trip"}
    - slot{"return_date": "2020-11-25"}
    - slot{"flight_stop_check": "true"}
    - slot{"email_id":"kareena.kapoor@bollywood.in"}
    - slot{"title":"Ms"}
    - slot{"user_name":"Kareena Kapoor"}
    - slot{"mobile_no":"8876345750"}
    - slot{"country_code":"91"}
    - form{"name": null}
    - slot{"requested_slot": null}
* quote{"quote_id": "2", "number": 2}
    - slot{"quote_id": "2"}
    - utter_booking
* affirm
    - action_booking_confirmation
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye
* goodbye

## interactive_story_8
* greet
    - utter_greet
* flight{"fromloc.city_name": "Bangalore", "toloc.city_name": "Frankfurt", "time": "2020-11-28T00:00:00.000+00:00", "depart_date.day_number": "28th", "depart_date.month_name": "November"}
    - slot{"fromloc.city_name": "Bangalore"}
    - slot{"time": "2020-11-28T00:00:00.000+00:00"}
    - slot{"toloc.city_name": "Frankfurt"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"fromloc.city_name": "Bangalore"}
    - slot{"toloc.city_name": "Frankfurt"}
    - slot{"fromloc.city_name": "Bangalore"}
    - slot{"toloc.city_name": "Frankfurt"}
    - slot{"requested_slot": "depart_date"}
* form: inform_departure_date{"depart_date.month_name": "November", "depart_date.day_number": "28th", "time": "2020-11-28T00:00:00.000+00:00"}
    - slot{"time": "2020-11-28T00:00:00.000+00:00"}
    - form: flight_booking_form
    - slot{"depart_date": "2020-11-28"}
    - slot{"requested_slot": "no_of_adults"}
* form: inform_no_of_adults{"no_of_adults": "2", "number": 2}
    - slot{"no_of_adults": "2"}
    - form: flight_booking_form
    - slot{"no_of_adults": "2"}
    - slot{"requested_slot": "child_passengers"}
* form: deny
    - form: flight_booking_form
    - slot{"child_passengers": false}
    - slot{"no_of_children": 0}
    - slot{"requested_slot": "infant_passengers"}
* form: deny
    - form: flight_booking_form
    - slot{"infant_passengers": false}
    - slot{"no_of_infants": 0}
    - slot{"requested_slot": "class_type"}
    - utter_ask_class_type
    - action_listen
* form: inform_class_type{"class_type": "BUSINESS"}
    - slot{"class_type": "BUSINESS"}
    - flight_booking_form
    - slot{"class_type": "BUSINESS"}
    - slot{"requested_slot": "currency_code"}
    - utter_ask_currency_code
    - action_listen
* form: inform_currency_code{"currency_code": "EUR"}
    - slot{"currency_code": "EUR"}
    - flight_booking_form
    - slot{"currency_code": "EUR"}
    - slot{"requested_slot": "round_trip"}
    - utter_ask_round_trip
    - action_listen
* form: inform_round_trip{"round_trip": "round trip"}
    - slot{"round_trip": "round trip"}
    - flight_booking_form
    - slot{"round_trip": "round trip"}
    - slot{"requested_slot": "return_date"}
* form: inform_return_date{"round_trip": "round trip", "time": "2020-12-16T00:00:00.000+00:00", "return_date.month_name": "December", "return_date.day_number": "16th"}
    - slot{"round_trip": "round trip"}
    - slot{"time": "2020-12-16T00:00:00.000+00:00"}
    - form: flight_booking_form
    - slot{"return_date": "2020-12-16"}
    - slot{"requested_slot": "flight_stop_check"}
* form: affirm
    - slot{"flight_stop_check": "true"}
    - form: flight_booking_form
    - slot{"requested_slot":"email_id"}
    - utter_ask_email_id
    - action_listen
* form: inform_email_id{"email_id":"matt.gunner@thyssenkrupp.de"}
    - slot{"email_id":"matt.gunner@thyssenkrupp.de"}
    - form: flight_booking_form
    - slot{"requested_slot":"title"}
    - utter_ask_title
    - action_listen
* form: inform_title{"title":"Mr"}
    - slot{"title":"Mr"}
    - form: flight_booking_form
    - slot{"requested_slot":"user_name"}
    - utter_ask_user_name
    - action_listen
* form: inform_user_name{"user_name":"Matthias Gunner"}
    - slot{"user_name":"Matthias Gunner"}
    - form: flight_booking_form
    - slot{"requested_slot":"mobile_no"}
    - utter_ask_mobile_no
    - action_listen
* form: inform_mobile_no{"mobile_no":"8876362750"}
    - slot{"mobile_no":"8876362750"}
    - form: flight_booking_form
    - slot{"requested_slot":"country_code"}
    - utter_ask_country_code
    - action_listen
* form: inform_country_code{"country_code":"49"}   
    - slot{"country_code":"49"}
    - form: flight_booking_form
    - slot{"fromloc.city_name": "Bangalore"}
    - slot{"toloc.city_name": "Frankfurt"}
    - slot{"depart_date": "2020-11-28"}
    - slot{"no_of_adults": "2"}
    - slot{"child_passengers": false}
    - slot{"infant_passengers": false}
    - slot{"class_type": "BUSINESS"}
    - slot{"currency_code": "EUR"}
    - slot{"round_trip": "round trip"}
    - slot{"return_date": "2020-12-16"}
    - slot{"flight_stop_check": "true"}
    - slot{"email_id":"matt.gunner@thyssenkrupp.de"}
    - slot{"title":"Mr"}
    - slot{"user_name":"Matthias Gunner"}
    - slot{"mobile_no":"8876362750"}
    - slot{"country_code":"49"}
    - form{"name": null}
    - slot{"requested_slot": null}
* quote{"quote_id": "1", "number": 1}
    - slot{"quote_id": "1"}
    - utter_booking
* affirm
    - action_booking_confirmation
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye
* goodbye
    - utter_goodbye

## interactive_story_1
* greet
    - utter_greet
* flight{"fromloc.city_name": "Bangalore", "toloc.city_name": "Dubai"}
    - slot{"fromloc.city_name": "Bangalore"}
    - slot{"toloc.city_name": "Dubai"}
    - flight_booking_form
    - form{"name": "flight_booking_form"}
    - slot{"fromloc.city_name": "Bangalore"}
    - slot{"toloc.city_name": "Dubai"}
    - slot{"fromloc.city_name": "Bangalore"}
    - slot{"toloc.city_name": "Dubai"}
    - slot{"requested_slot": "depart_date"}
* form: inform_departure_date{"depart_date.month_name": "October", "depart_date.day_number": "5th", "time": "2020-10-05T00:00:00.000+00:00"}
    - slot{"time": "2020-10-05T00:00:00.000+00:00"}
    - form: flight_booking_form
    - slot{"depart_date": "2020-10-05"}
    - slot{"requested_slot": "no_of_adults"}
* form: inform_no_of_adults{"no_of_adults": "3", "number": 3}
    - slot{"no_of_adults": "3"}
    - form: flight_booking_form
    - slot{"no_of_adults": "3"}
    - slot{"requested_slot": "child_passengers"}
* form: deny
    - form: flight_booking_form
    - slot{"child_passengers": false}
    - slot{"no_of_children": 0}
    - slot{"requested_slot": "infant_passengers"}
* form: affirm
    - form: flight_booking_form
    - slot{"infant_passengers": true}
    - slot{"requested_slot": "no_of_infants"}
* form: inform_no_of_infants{"no_of_infants": "2", "number": 2}
    - slot{"no_of_infants": "2"}
    - form: flight_booking_form
    - slot{"no_of_infants": "2"}
    - slot{"requested_slot": "class_type"}
    - utter_ask_class_type
    - action_listen
* form: inform_class_type{"class_type": "ECONOMY"}
    - slot{"class_type": "ECONOMY"}
    - flight_booking_form
    - slot{"class_type": "ECONOMY"}
    - slot{"requested_slot": "currency_code"}
    - utter_ask_currency_code
    - action_listen
* form: inform_currency_code{"currency_code": "INR"}
    - slot{"currency_code": "INR"}
    - flight_booking_form
    - slot{"currency_code": "INR"}
    - slot{"requested_slot": "round_trip"}
    - utter_ask_round_trip
    - action_listen
* form: inform_round_trip{"round_trip": "one way"}
    - slot{"round_trip": "one way"}
    - flight_booking_form
    - slot{"round_trip": "one way"}
    - slot{"requested_slot": "flight_stop_check"}
* form: deny
    - form: flight_booking_form
    - slot{"flight_stop_check": "false"}
    - slot{"requested_slot": "email_id"}
* form: inform_email_id{"email_id": "david@daveabraham.me"}
    - slot{"email_id": "david@daveabraham.me"}
    - form: flight_booking_form
    - slot{"email_id": "david@daveabraham.me"}
    - slot{"requested_slot": "title"}
    - utter_ask_title
* greet{"title": "Mr"}
    - slot{"title": "Mr"}
    - utter_ask_user_name
    - action_listen
* form: inform_user_name{"user_name": "David Abraham"}
    - slot{"user_name": "David Abraham"}
    - flight_booking_form
    - slot{"user_name": "David Abraham"}
    - slot{"requested_slot": "mobile_no"}
* form: inform_mobile_no{"mobile_no": "9850369780", "number": "9850369780"}
    - slot{"mobile_no": "9850369780"}
    - form: flight_booking_form
    - slot{"mobile_no": "9850369780"}
    - slot{"requested_slot": "country_code"}
* form: inform_country_code{"country_code": "91", "number": "91"}
    - slot{"country_code": "91"}
    - form: flight_booking_form
    - slot{"country_code": "91"}
    - form{"name": null}
    - slot{"requested_slot": null}
* quote{"quote_id": "3", "number": 3}
    - slot{"quote_id": "3"}
    - utter_booking
* affirm
    - action_booking_confirmation
    - utter_confirm
    - action_slot_reset
    - reset_slots
    - utter_goodbye
* goodbye

## pnr_retrieval_story_1
* inform_pnr
    - retrieve_booking_info_form
    - form{"name":"retrieve_booking_info_form"}
    - slot{"requested_slot":"pnr"}
    - utter_ask_pnr
    - action_listen
* inform_pnr{"pnr":"PNRc3c2"}
    - slot{"pnr":"PNRc3c2"}
    - utter_wait_pnr
    - form: retrieve_booking_info_form
    - slot{"title":"Mr"}
    - slot{"user_name":"David Abraham"}
    - slot{"email_id":"daveynoire79@gmail.com"}
    - slot{"country_code":"1"}
    - slot{"mobile_no":"7739345979"}
    - form{"name":null}
    - slot{"requested_slot": null}
    - utter_other_help

## pnr_retrieval_story_2
* inform_pnr{"pnr":"PNR59a6"}
    - slot{"pnr":"PNR59a6"}
    - utter_wait_pnr
    - retrieve_booking_info_form
    - slot{"title":"Mr"}
    - slot{"user_name":"John Doe"}
    - slot{"email_id":"john.doe@gmail.com"}
    - slot{"country_code":"65"}
    - slot{"mobile_no":"7777345979"}
    - form{"name":"retrieve_booking_info_form"}
    - form{"name":null}
    - slot{"requested_slot": null}
    - utter_other_help

## pnr_retrieval_story_3
* greet
    - utter_greet
* inform_pnr{"pnr":"PNRf13e"}
    - slot{"pnr":"PNRf13e"}
    - utter_wait_pnr
    - retrieve_booking_info_form
    - slot{"title":"Ms"}
    - slot{"user_name":"Mary Jane"}
    - slot{"email_id":"mary.jane@marvelinc.org"}
    - slot{"country_code":"97"}
    - slot{"mobile_no":"9999345979"}
    - form{"name":"retrieve_booking_info_form"}
    - form{"name":null}
    - slot{"requested_slot": null}
    - utter_other_help

## pnr_retrieval_story_4
* inform_pnr
    - retrieve_booking_info_form
    - form{"name":"retrieve_booking_info_form"}
    - slot{"requested_slot":"pnr"}
    - utter_ask_pnr
    - action_listen
* inform_pnr{"pnr":"PNRl18e"}
    - slot{"pnr":"PNRl18e"}
    - utter_wait_pnr
    - form: retrieve_booking_info_form
    - slot{"title":"Mr"}
    - slot{"user_name":"Keanu Reeves"}
    - slot{"email_id":"keanreeves@matrix.com"}
    - slot{"country_code":"1"}
    - slot{"mobile_no":"7739345985"}
    - form{"name":null}
    - slot{"requested_slot": null}
    - utter_other_help

## pnr_retrieval_story_5
* greet
    - utter_greet
* inform_pnr{"pnr": "PNR5a7d", "number": "7"}
    - slot{"pnr": "PNR5a7d"}
    - utter_wait_pnr
    - retrieve_booking_info_form
    - form{"name": "retrieve_booking_info_form"}
    - slot{"pnr": "PNR5a7d"}
    - slot{"title": "Ms"}
    - slot{"user_name": "Jane Doe"}
    - slot{"email_id": "jane.doe@boringclerk.com"}
    - slot{"country_code": "95"}
    - slot{"mobile_no": "7739345987"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_other_help

## pnr_retrieval_story_6
* greet
    - utter_greet
* inform_pnr
    - retrieve_booking_info_form
    - form{"name": "retrieve_booking_info_form"}
    - slot{"requested_slot": "pnr"}
* form: inform_pnr{"pnr": "PNR5a7d", "number": "7"}
    - slot{"pnr": "PNR5a7d"}
    - form: retrieve_booking_info_form
    - slot{"pnr": "PNR5a7d"}
    - slot{"title": "Mr"}
    - slot{"user_name": "David Abraham"}
    - slot{"email_id": "davi@davidabraham.me"}
    - slot{"country_code": 91}
    - slot{"mobile_no": 9450368750}
    - slot{"pnr": null}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_other_help
* deny
    - utter_goodbye

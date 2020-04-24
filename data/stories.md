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
  - action_flight_search
* quote
  - utter_booking
>check_price_search


## flight booking confirmed
>check_price_search
* affirm
  - utter_confirm
  - utter_goodbye

## flight booking cancelled
>check_price_search
* deny
  - utter_cancellation
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
  - utter_goodbye

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

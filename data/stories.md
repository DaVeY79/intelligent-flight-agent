<!-- ## flight query
* flight
  - utter_flight

## flight time query
* flight_time
  - utter_flight_time

## utter_airfare
* airfare
  - utter_airfare

## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye -->

## say hello
* greet
  - utter_greet
>check_greeting

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot


## flight booking confirmed
* greet
  - utter_greet
* flight
  - action_flight_search
  - utter_booking
* affirm
  - utter_confirm
  - utter_goodbye

## flight booking confirmed direct
* flight
  - action_flight_search
  - utter_booking
* affirm
  - utter_confirm
  - utter_goodbye

## flight booking cancelled
* greet
  - utter_greet
* flight
  - action_flight_search
  - utter_booking
* deny
  - utter_cancellation
  - utter_goodbye

## flight booking cancelled direct
* flight
  - action_flight_search
  - utter_booking
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

## user accepts information is helpful
>check_greeting
>check_info_helpful
* affirm
  - utter_happy
  - utter_goodbye

## user denies information is helpful
>check_greeting
>check_info_helpful
* deny
  - utter_unhappy
  - utter_goodbye


## flight time query
* flight_time
  - utter_flight_time

## utter_airfare
* airfare
  - utter_airfare

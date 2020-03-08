## flight booking confirmed
* greet
    - utter_greet
* flight
    - action_flight_search   <!-- predicted: utter_flight -->
    - utter_booking   <!-- predicted: action_listen -->
    - action_listen   <!-- predicted: utter_flight -->
* affirm
    - utter_confirm   <!-- predicted: action_listen -->


## flight booking confirmed direct
* flight
    - action_flight_search   <!-- predicted: utter_flight -->
    - utter_booking   <!-- predicted: action_listen -->
    - action_listen   <!-- predicted: utter_flight -->
* affirm
    - utter_confirm   <!-- predicted: action_listen -->


## flight booking cancelled
* greet
    - utter_greet
* flight
    - action_flight_search   <!-- predicted: utter_flight -->
    - utter_booking   <!-- predicted: action_listen -->
    - action_listen   <!-- predicted: utter_flight -->
* deny
    - utter_cancellation   <!-- predicted: action_listen -->


## flight information happy path
* greet
    - utter_greet
* flight+airfare
    - utter_flight+airfare   <!-- predicted: utter_cheer_up -->
    - utter_acknowledge_help   <!-- predicted: utter_did_that_help -->
    - action_listen   <!-- predicted: utter_happy -->
* affirm
    - utter_happy   <!-- predicted: action_listen -->


## flight information unhappy path
* greet
    - utter_greet
* greet
    - utter_greet
* flight+airfare
    - utter_flight+airfare   <!-- predicted: utter_cheer_up -->
    - utter_acknowledge_help   <!-- predicted: utter_did_that_help -->
    - action_listen   <!-- predicted: utter_happy -->
* deny
    - utter_unhappy   <!-- predicted: action_listen -->



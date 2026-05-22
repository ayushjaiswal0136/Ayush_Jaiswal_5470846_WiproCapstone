Feature: Bus Search Functionality Validations

  Background:
    Given User launches MakeMyTrip application
    When User closes the login popup
    And User navigates to the Bus section

  # POSITIVE TESTS
  @positive @search
  Scenario: Verify that searched route information displayed correctly
    Given User extracts test data from CSV "bus_search_data.csv" for row "1"
    When User provides search source city from CSV
    And User provides search destination city from CSV
    And User selects a travel date
    And User clicks on Search Buses button
    Then User should see the correct route from CSV on results page

  @positive @search
  Scenario: Assert whether sleeper filter is applied successfully
    Given User extracts test data from CSV "bus_search_data.csv" for row "1"
    When User provides search source city from CSV
    And User provides search destination city from CSV
    And User selects a travel date
    And User clicks on Search Buses button
    And User applies the Sleeper filter
    Then Verify that the results update successfully

  @positive @search
  Scenario: Assert seat number selection
    Given User extracts test data from CSV "bus_search_data.csv" for row "1"
    When User provides search source city from CSV
    And User provides search destination city from CSV
    And User selects a travel date
    And User clicks on Search Buses button
    And User selects an available bus
    And User selects a specific seat to verify
    Then Verify that a selected seat number is displayed

  @positive @search
  Scenario: Assert Booking Page details are correct
    Given User extracts test data from CSV "bus_search_data.csv" for row "1"
    When User provides search source city from CSV
    And User provides search destination city from CSV
    And User selects a travel date
    And User clicks on Search Buses button
    And User selects an available bus
    And User selects a specific seat to verify
    Then User should see the booking page with correct route details from CSV

  # NEGATIVE TESTS
  @negative @search
  Scenario: Verify that buses are not displayed for same source and destination
    Given User extracts test data from CSV "negative_bus_search_data.csv" for row "1"
    When User provides search source city from CSV
    And User provides search destination city from CSV
    And User clicks on Search Buses button
    Then User should see an error message for same source and destination

  @negative @search
  Scenario: Verify that No Buses Found message is displayed when invalid route selected
    Given User extracts test data from CSV "no_bus_route_data.csv" for row "1"
    When User provides search source city from CSV
    And User provides search destination city from CSV
    And User selects a travel date
    And User clicks on Search Buses button
    Then User should see a No Buses Found message
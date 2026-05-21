Feature: End-to-End Bus Booking Workflow

  @e2e
  Scenario: Successfully search, select, and proceed to payment for a bus ticket
    Given User launches MakeMyTrip application
    And User loads test data from Excel "bus_e2e_data.xlsx"
    When User closes the login popup
    And User navigates to the Bus section
    And User enters source city from Excel
    And User enters destination city from Excel
    And User selects a travel date
    And User clicks on Search Buses button
    And User applies the AC filter
    And User selects an available bus
    And User selects a specific seat
    And User verifies boarding and dropping points
    And User enters passenger details from Excel
    And User proceeds to payment page
    And User enters card details from Excel
    Then Close the browser
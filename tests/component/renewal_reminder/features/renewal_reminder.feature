@fixture.controller.telegram_api
Feature: Renewal Reminder

  Background:
    Given Telegram API is available

  @success
  Scenario: Renewals are due
    Given the file contains
      | name    | grade | licence expiry |
      | person1 | 1 dan | 2              |
    When renewal reminder is executed with 1 day notice
    Then Telegram API receives request containing "No renewals due."

  @negative
  Scenario: Renewals are due
    Given the file contains
      | name    | grade | licence expiry |
      | person1 | 1 dan | 2              |
      | person2 | 1 kyu | 1              |
      | person3 | 9 kyu | 0             |
    When renewal reminder is executed with 1 day notice
    Then Telegram API receives request containing "There are 2 renewals due in the next 1 day(s)."
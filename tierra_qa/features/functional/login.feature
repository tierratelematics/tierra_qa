Feature: Login
    A user login try to login to the application

    Scenario: Successful login
        Given When I log in as Administrator
        Then I am logged in

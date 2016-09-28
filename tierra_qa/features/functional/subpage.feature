Feature: Subpage
    A logged in user login visit a subpage

    Scenario: Visit subpage
        Given I am logged in as Administrator
        When I visit the HelloPage page
        Then I land on the HelloPage page

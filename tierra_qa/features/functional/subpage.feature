Feature: Subpage
    A logged in user login visit a subpage

    Scenario: Visit subpage
        # Given When I log in as Administrator
        # And I visit the HelloPage page
        Given I visit the HelloPage page
        Then I am on the HelloPage page

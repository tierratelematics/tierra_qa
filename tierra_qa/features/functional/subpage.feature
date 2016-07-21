Feature: Subpage
    A logged in user login visit a subpage

    Scenario: Visit subpage
        # Given When I log in as Administrator
        # And I visit the example page
        Given I visit the example page
        Then I am on the example page

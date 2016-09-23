"""
Base page implementation
========================

This is where the base page implementation lives.
"""
from pypom import Page


class BasePage(Page):
    """
        This is the base page to be used in tierra_qa.

        Once you clone tierra_qa for your own qa project, you should:

        * implement the login, is_loggedin and logout methods of this class
        * add your own page object classes depending on your business
          logics inheriting from this base class
    """

    def login(self, username, password):
        """
            This is the login method of the base page object.

            It's up to you implement this method once you cloned
            tierra_qa.
        """
        pass

    def is_loggedin(self):
        """
            This is the is_loggedin method of the base page object.

            It's up to you implement this method once you cloned
            tierra_qa.

            :return: True if you are logged in or False
            :rtype: bool
        """
        pass

    def logout(self):
        """
            This is the logout method of the base page object.

            It's up to you implement this method once you cloned
            tierra_qa.
        """
        pass

    @property
    def current_url(self):
        """
            Returns the current url

            :return: current_url of the driver instance
            :rtype: str
        """
        return self.driver.url

"""
Base page implementation
========================

This is where the base page implementation lives.
"""

from pypom_form.form import BaseFormPage


class BasePage(BaseFormPage):
    """
        This is the base page to be used in tierra_qa.

        Once you clone tierra_qa for your own qa project, you should:

        * implement the login, is_loggedin and logout methods of this class
        * add your own page object classes depending on your business
          logics inheriting from this base class
    """
    navigation = None

    def login(self, username, password):
        """
            This is the login method of the base page object.

            It's up to you implement this method once you cloned
            tierra_qa.

            :return: BasePage instance
            :rtype: object
        """

    def is_loggedin(self):
        """
            This is the is_loggedin method of the base page object.

            It's up to you implement this method once you cloned
            tierra_qa.

            :return: True if you are logged in or False
            :rtype: bool
        """
        return True

    def username(self):
        """
            This is the username method of the base page object.

            It's up to you implement this method once you cloned
            tierra_qa.

            :return: the username or None
            :rtype: string or None
        """
        return 'admin'

    def logout(self):
        """
            This is the logout method of the base page object.

            It's up to you implement this method once you cloned
            tierra_qa.

            :return: BasePage instance
            :rtype: object
        """

    @property
    def current_url(self):
        """
            Returns the current url

            :return: current_url of the driver instance
            :rtype: str
        """
        return self.driver.url

    def wait_for_url_change(self, url):
        """
            Wait for url change occurred.

            :return: BasePage instance
            :rtype: object
        """
        self.wait.until(lambda s: self.current_url != url)
        return self

    def has_text(self, text):
        """
            Check for text in page.

            :return: True if the given text is present
            :rtype: bool
        """
        return self.driver.is_text_present(text, wait_time=self.timeout)

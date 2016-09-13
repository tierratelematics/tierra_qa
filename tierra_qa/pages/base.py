from pypom import Page


class BasePage(Page):
    """ This is the base page to be used in tierra_qa """

    def login(self):
        # it's up to you implement the login logics
        pass

    def is_loggedin(self):
        # it's up to you implement the is loggedin logics
        pass

    def logout(self):
        # it's up to you implement the is loggedin logics
        pass

    @property
    def current_url(self):
        """ Returns the current url """
        return self.driver.url

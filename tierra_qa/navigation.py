try:
    from urlparse import urljoin
except ImportError:
    # python3 compatibility
    from urllib.parse import urljoin

from tierra_qa.util import (
    get_page_class,
    get_page_url,
)


class Navigation(object):
    page_id = None

    def __init__(self,
                 page,
                 default_page_class,
                 page_mappings,
                 credentials_mapping,
                 skin,
                 base_url):
        self.setPage(page)
        self.default_page_class = default_page_class
        self.page_mappings = page_mappings
        self.credentials_mapping = credentials_mapping
        self.skin = skin
        self.base_url = base_url

    def setPage(self, page, page_id=None):
        """ Set wrapping page and update reference links
            for page and navigation
        """
        page.navigation = self
        self.page = page
        self.page_id = page_id

    def visit_page(self, page_id, **kwargs):
        """ Visit page id reference in navigation
            class
        """
        page_class = self.get_page_class(page_id=page_id)
        page_instance = page_class(self.page.driver, **kwargs)
        page_url = urljoin(self.base_url, self.get_page_url(page_id))

        page_instance.driver.visit(page_url)
        self.setPage(page_instance, page_id=page_id)
        return page_instance

    def get_page_url(self, page_id):
        """ Return the page url for the current wrapped page """
        return get_page_url(self.skin,
                            self.page_mappings, page_id)

    def get_credentials(self, user_id):
        """ Return a tuple with username and password for the given
            user_id
        """
        user_credentials = self.credentials_mapping[user_id]
        return user_credentials['username'], user_credentials['password']

    def get_page_class(self, page_id=None, fallback=None):
        """ Return the page class """
        fallback = fallback and fallback or self.default_page_class
        return get_page_class(
            self.skin,
            self.page_mappings,
            page_id=page_id,
            fallback=fallback)

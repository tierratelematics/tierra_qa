try:
    from urlparse import urljoin
except ImportError:
    # python3 compatibility
    from urllib.parse import urljoin

from .config import DEFAULT_PAGES


def get_page_url(skin_name, page_mappings, page_id):
    """ Returns the page_url for the given page_id and skin_name """
    fallback = '/'
    if page_id is not None:
        return page_mappings[page_id].get('path', '/')
    return fallback


def get_page_class(skin_name, page_mappings, page_id=None, fallback=None):
    """ Returns the page class for a given skin name and page mapping.

        First of all, if there is no page id it will return the given fallback
        if defined of the default page for the skin in use.

        If there is a page id, it will return:
        * the match for the given skin if defined
        * a fallback if defined
        * the given fallback if defined or the global default page class
    """
    fallback = fallback and fallback or lookup_dotted_path(DEFAULT_PAGES[
        skin_name])
    if not page_id:
        return fallback

    page_class_mapping = page_mappings[page_id].get('page_class', None)
    if page_class_mapping is not None:
        result = page_class_mapping.get(
            skin_name, page_class_mapping.get('fallback', None))
        return result and lookup_dotted_path(result) or fallback

    return fallback


def page_factory(base_url, browser, default_page_class, page_mappings,
                 page_id=None, **kwargs):
    url = base_url

    if page_id is None:
        url = base_url
        page_class = default_page_class
    else:
        # TODO: get page url
        # TODO: get page class
        path = page_mappings[page_id]['path']
        page_class = get_page_class(
            page_id=page_id, fallback=default_page_class)
        url = urljoin(base_url, path)

    page = page_class(browser, base_url=url, **kwargs)

    return page


def lookup_dotted_path(dotted):
    """ Lookup a class for a given dotted path.

         This might help preventing circular import issues in configuration
         files.
    """
    components = dotted.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

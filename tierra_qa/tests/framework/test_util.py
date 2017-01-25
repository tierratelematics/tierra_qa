import pytest
import tierra_qa


@tierra_qa.testing.framework
@pytest.mark.parametrize("dotted,mod", [
    ('tierra_qa.pages.BasePage', tierra_qa.pages.BasePage,),
    ('tierra_qa.pages.base.BasePage', tierra_qa.pages.BasePage,),
    ('tierra_qa', tierra_qa,),
])
def test_dotted(dotted, mod):
    """ """
    from tierra_qa.util import lookup_dotted_path

    assert lookup_dotted_path(
        dotted) == mod


def test_get_page_class1():
    """ page mapping without page_class"""
    from tierra_qa.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {'path': '/'},
    }

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id) == tierra_qa.pages.BasePage


def test_get_page_class2():
    """ page mapping with non matching skin, no fallback """
    from tierra_qa.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {
            'path': '/',
            'page_class': {'skin2': 'tierra_qa.pages'}
        },
    }

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id) == tierra_qa.pages.BasePage


def test_get_page_class3():
    """ page mapping with non matching skin, with fallback """
    from tierra_qa.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {
            'path': '/',
            'page_class': {
                'skin2': 'tierra_qa.pages',
                'fallback': 'tierra_qa',
            }
        },
    }

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id) == tierra_qa


def test_get_page_class4():
    """ page mapping without non matching skin.
        Fallback in config ovverrides passed fallback.
    """
    from tierra_qa.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {
            'path': '/',
            'page_class': {
                'skin2': 'tierra_qa.pages',
                'fallback': 'tierra_qa',
            }
        },
    }

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id,
        fallback=tierra_qa.pages) == tierra_qa


def test_get_page_class5():
    """ page mapping with non matching skin.
        Fallback in config wins against default page
        class (no fallback in conf)
    """
    from tierra_qa.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {
            'path': '/',
            'page_class': {
                'skin2': 'tierra_qa',
            }
        },
    }

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id,
        fallback=tierra_qa.pages) == tierra_qa.pages


def test_get_page_class6():
    """ page mapping with matching skin.
    """
    from tierra_qa.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {
            'path': '/',
            'page_class': {
                'skin1': 'tierra_qa',
            }
        },
    }

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id,
        fallback=tierra_qa.pages) == tierra_qa

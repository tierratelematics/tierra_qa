"""
Page mappings config
--------------------
Here you can define all your page mappings with path and optionally a
class_page if you want your specific page object implementation.
By default the :py:class:`tierra_qa.pages.BasePage` will be instanciated.

For example you could configure your own page object implementations:

.. code-block:: python

    PAGE_MAPPINGS = {
        'HomePage': {'path': '/'},
        'HelloPage': {'path': '/hello'},
        'AnotherPage': {'path': '/anotherpage', 'class_page': AnotherPage},
        }

"""
PAGE_MAPPINGS = {
    'HomePage': {'path': '/'},
    'HelloPage': {'path': '/hello'},
    }

Fixture Diagrams
=================================
The following diagram shows the interactions between the `pytest fixtures`_ created in the ``tierra_qa`` package:

.. graphviz::

   digraph {
      base_url [color="grey"];
      browser [color="grey"];
      request [color="grey"];
      base_url -> {page} [color="grey"];
      browser -> {page} [color="grey"];
      request -> {page credentials_mapping username password} [color="grey"];
      credentials_mapping -> {username password}
      username -> {page};
      password -> {page};
      page_mappings -> {page};
      default_page_class -> {page};
   }


.. _pytest fixtures: http://doc.pytest.org/en/latest/fixture.html


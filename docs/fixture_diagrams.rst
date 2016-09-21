Fixture Diagrams
=================================
The following diagram shows the interactions between the `pytest fixtures`_ created in the ``tierra_qa`` package:

.. graphviz::

   digraph {
      page [shape=box];
      variables [color="red"];
      request -> {username password credentials_mapping page};
      variables -> credentials_mapping;
      credentials_mapping -> {username password};
      username -> page;
      password -> page;
      base_url -> page;
      browser -> page;
      page_mappings -> page;
      default_page_class -> page; 
   }


.. _pytest fixtures: http://doc.pytest.org/en/latest/fixture.html


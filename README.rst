django-query-parameters
=======================

Adds two template tags that simplify the manipulation of GET parameters on a querystring. Allows easy addition, manipulation, and deletion of parameters onto an existing querystring.

The module is comprised of two template tags: `set_query_parameters` and `del_query_parameters`. 

set_query_parameters
--------------------

Takes a 1+ list of key=value pairs and generates an updated querystring that includes those pairs. If a key does not already exist in the querystring, it will be added. If a key exists, it will be updated with the new value

    # current page is http://localhost/?page=1&limit=20
    {% load query_parameters %}
    {% set_query_parameters page=2 order=desc %} # => page=2&limit=20&order=desc

del_query_parameters
--------------------

Takes a 1+ list of keys and generates an updated querystring that removes those keys.

    # current page is http://localhost/?page=1&limit=20
    {% load query_parameters %}
    {% del_query_parameters page order %} # => limit=20
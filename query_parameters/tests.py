from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template import Template
from django.template import Context
from django.template import RequestContext
from django.test.client import Client
from django.http import HttpRequest
from django.http import QueryDict

class SetQueryParametersTestCase(TestCase):
    def test_empty_querystring(self):
        t = Template(
                '{% load query_parameters %}'
                '{% set_query_parameters prop1=val1 %}'
            )
        request = HttpRequest()
        request.GET = QueryDict('')

        c = RequestContext(request)
        result = t.render(c)
        self.assertEqual(result, 'prop1=val1')

    def test_new_property(self):
        t = Template(
                '{% load query_parameters %}'
                '{% set_query_parameters prop1=val1 %}'
            )
        request = HttpRequest()
        request.GET = QueryDict('prop2=val2')

        c = RequestContext(request)
        result = t.render(c)
        self.assertEqual(result, 'prop1=val1&prop2=val2')

    def test_invalid_parameters(self):
        from django.template import TemplateSyntaxError
        self.assertRaises(TemplateSyntaxError, Template, '{% load query_parameters %}{% set_query_parameters prop1 %}')

    def test_multiple_new_properties(self):
        t = Template(
                '{% load query_parameters %}'
                '{% set_query_parameters prop1=val1 prop2=val2 %}'
            )
        request = HttpRequest()
        request.GET = QueryDict('prop3=val3')

        c = RequestContext(request)
        result = t.render(c)
        self.assertEqual(result, 'prop1=val1&prop2=val2&prop3=val3')

    def test_update_property(self):
        t = Template(
                '{% load query_parameters %}'
                '{% set_query_parameters prop1=val1 %}'
            )
        request = HttpRequest()
        request.GET = QueryDict('prop1=val2')

        c = RequestContext(request)
        result = t.render(c)
        self.assertEqual(result, 'prop1=val1')


    def test_overwriting_properties(self):
        t = Template(
                '{% load query_parameters %}'
                '{% set_query_parameters prop1=val1 prop1=val2 %}'
            )
        request = HttpRequest()
        request.GET = QueryDict('prop1=val3')

        c = RequestContext(request)
        result = t.render(c)
        self.assertEqual(result, 'prop1=val2')



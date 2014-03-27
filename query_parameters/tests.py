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
        result = self.template_generator(
                query_string='', 
                set_query_parameters_value='prop1=val1'
        )
        self.assertEqual(result, 'prop1=val1')

    def test_new_property(self):
        result = self.template_generator(
                query_string='prop2=val2', 
                set_query_parameters_value='prop1=val1'
        )
        self.assertEqual(result, 'prop1=val1&prop2=val2')

    def test_invalid_parameters(self):
        from django.template import TemplateSyntaxError
        self.assertRaises(TemplateSyntaxError, Template, '{% load query_parameters %}{% set_query_parameters prop1 %}')

    def test_multiple_new_properties(self):
        result = self.template_generator(
                query_string='prop3=val3',
                set_query_parameters_value='prop1=val1 prop2=val2'
        )
        self.assertEqual(result, 'prop1=val1&prop2=val2&prop3=val3')

    def test_update_property(self):
        result = self.template_generator(
                query_string='prop1=val2', 
                set_query_parameters_value='prop1=val1'
        )
        self.assertEqual(result, 'prop1=val1')

    def test_update_and_add_property(self):
        result = self.template_generator(
                query_string='prop1=val1&prop2=val2', 
                set_query_parameters_value='prop1=val1_modified prop3=val3'
        )
        self.assertEqual(result, 'prop1=val1_modified&prop2=val2&prop3=val3')

    def template_generator(self, query_string, set_query_parameters_value):
        """
        Helper method to simplify generating a template with a mock `query_string` and `set_query_parameters_value`
        """
        t = Template(
                '{% load query_parameters %}'
                '{% set_query_parameters ' + set_query_parameters_value + ' %}'
            )
        request = HttpRequest()
        request.GET = QueryDict(query_string)

        c = RequestContext(request)
        result = t.render(c)
        return result


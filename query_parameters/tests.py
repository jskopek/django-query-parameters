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

    def test_add_nothing(self):
        result = self.template_generator(
                query_string='prop2=val2', 
                set_query_parameters_value=''
        )
        self.assertEqual(result, 'prop2=val2')

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

    def test_illegal_variable_name(self):
        result = self.template_generator(
                query_string='',
                set_query_parameters_value='_prop1=val1'
        )
        self.assertEqual(result, '_prop1=val1')


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

    def test_save_in_context(self):
        t = Template(
                '{% load query_parameters %}'
                '{% set_query_parameters prop1=val1 as=result %}'
            )
        request = HttpRequest()
        request.GET = QueryDict('prop2=val2')

        c = RequestContext(request)
        result = t.render(c)
        self.assertEqual(result, '')
        self.assertEqual(c['result'], 'prop1=val1&prop2=val2')

    def test_load_from_context(self):
        t = Template(
                '{% load query_parameters %}'
                '{% set_query_parameters prop1=val1 with=existing_querystring %}'
            )
        request = HttpRequest()
        request.GET = QueryDict('prop2=val2')

        c = RequestContext(request, {'existing_querystring':'prop3=val3'})
        result = t.render(c)
        self.assertEqual(result, 'prop1=val1&prop3=val3')

    def test_context_chaining(self):
        t = Template(
                '{% load query_parameters %}'
                '{% set_query_parameters prop1=val1 as=result %}'
                '{% set_query_parameters prop3=val3 with=result as=modified_result %}'
            )
        request = HttpRequest()
        request.GET = QueryDict('prop2=val2')

        c = RequestContext(request)
        result = t.render(c)
        self.assertEqual(result, '')
        self.assertEqual(c['result'], 'prop1=val1&prop2=val2')
        self.assertEqual(c['modified_result'], 'prop1=val1&prop2=val2&prop3=val3')

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



class DelQueryParametersTestCase(TestCase):
    def test_empty_querystring(self):
        result = self.template_generator(
                query_string='',
                del_query_parameters_value='prop1'
        )
        self.assertEqual(result, '')

    def test_delete_querystring(self):
        result = self.template_generator(
                query_string='prop1=value1',
                del_query_parameters_value='prop1'
        )
        self.assertEqual(result, '')

    def test_delete_querystring_with_remainders(self):
        result = self.template_generator(
                query_string='prop1=value1&prop2=value2',
                del_query_parameters_value='prop1'
        )
        self.assertEqual(result, 'prop2=value2')

    def test_delete_multiple_querystrings_with_remainders(self):
        result = self.template_generator(
                query_string='prop1=value1&prop2=value2&prop3=value3',
                del_query_parameters_value='prop1 prop2'
        )
        self.assertEqual(result, 'prop3=value3')

    def test_delete_nothing(self):
        result = self.template_generator(
                query_string='prop1=value1',
                del_query_parameters_value=''
        )
        self.assertEqual(result, 'prop1=value1')

    def test_delete_in_context(self):
        t = Template(
                '{% load query_parameters %}'
                '{% del_query_parameters prop2 as=a_result %}'
            )
        request = HttpRequest()
        request.GET = QueryDict('prop1=val1&prop2=val2')

        c = RequestContext(request)
        result = t.render(c)
        self.assertEqual(result, '')
        self.assertEqual(c['a_result'], 'prop1=val1')

    def test_load_from_context(self):
        t = Template(
                '{% load query_parameters %}'
                '{% del_query_parameters prop1 with=existing_querystring %}'
            )
        request = HttpRequest()
        request.GET = QueryDict('prop2=val2')

        c = RequestContext(request, {'existing_querystring':'prop3=val3&prop1=val1'})
        result = t.render(c)
        self.assertEqual(result, 'prop3=val3')

    def template_generator(self, query_string, del_query_parameters_value):
        """
        Helper method to simplify generating a template with a mock `query_string` and `del_query_parameters_value`
        """
        t = Template(
                '{% load query_parameters %}'
                '{% del_query_parameters ' + del_query_parameters_value + ' %}'
            )
        request = HttpRequest()
        request.GET = QueryDict(query_string)

        c = RequestContext(request)
        result = t.render(c)
        return result


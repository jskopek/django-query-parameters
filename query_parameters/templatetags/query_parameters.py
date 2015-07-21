from django import template
from django.http import QueryDict
from django.conf import settings
import re

register = template.Library()

# SETTING PARAMETERS
@register.tag
def set_query_parameters(parser, token):
    """
    Takes a 1+ list of key=value pairs and generates an updated querystring that includes those pairs. If a key does not already exist
    in the querystring, it will be added. If a key exists, it will be updated with the new value

    e.g. querystring = http://localhost/?page=1&limit=20
    {% set_query_parameters page=2 order=desc %} => page=2&limit=20&order=desc
    """

    params = token.split_contents()[1:]

    # check to see if a special variable output key has been passed (default to `as`); 
    # if so, we will store the result in the context variable define by the value
    VARIABLE_OUTPUT_KEY = getattr(settings, 'QUERY_PARAMETERS_VARIABLE_OUTPUT_KEY', 'as')
    params, as_var = pluck_property(params, VARIABLE_OUTPUT_KEY)

    # check to see if a special variable input key has been passed (default to `with`); 
    # if so, we will pull the query string from the context variable defined by the value
    VARIABLE_INPUT_KEY = getattr(settings, 'QUERY_PARAMETERS_VARIABLE_INPUT_KEY', 'with')
    params, with_var = pluck_property(params, VARIABLE_INPUT_KEY)

    try:
        key_value_dict = dict(key_value_pair.split('=') for key_value_pair in params)
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires arguments to be in `key=value` pairs' % token.contents.split()[0])

    return QueryStringSetNode(key_value_dict, as_var, with_var)

class QueryStringSetNode(template.Node):
    def __init__(self, parameter_dict, as_var, with_var):
        self.parameter_dict = parameter_dict
        self.as_var = as_var
        self.with_var = with_var

    def contextual_parameter_dict(self, context):
        """
        Searches the context for any variables named after the provided parameters; if any found,
        replaces the parameter name with the corresponding variable value

        e.g.
        first_property = 'test'
        {first_property: 'value_1', 'key_2': first_property} => {'test': 'value_1', 'key_2': 'test'}
        """

        value_parameter_dict = {}
        for key, value in self.parameter_dict.items():
            value_parameter_dict[key] = get_value(value, context)
        return value_parameter_dict

    def render(self, context):
        # if we have been passed a querystring from the context, load it; otherwise, pull from the context
        if self.with_var:
            query_string = get_value(self.with_var, context)
        else:
            query_string = get_query_string(context)

        existing_query_dict = QueryDict(query_string).copy()
        for key, value in self.contextual_parameter_dict(context).items():
            existing_query_dict[key] = value

        result = existing_query_dict.urlencode()

        # if we are storing result as a context property, do so and reutrn a blank string; otherwise, return the value
        if self.as_var:
            context[self.as_var] = result
            return ''
        else:
            return result

# DELETING PARAMETERS
@register.tag
def del_query_parameters(parser, token):
    """
    Takes a 1+ list of keys and generates an updated querystring that removes those keys.

    e.g. querystring = http://localhost/?page=1&limit=20
    {% del_query_parameters page order %} => limit=20
    """

    params = token.split_contents()[1:]

    # check to see if a special variable output key has been passed (default to `as`); 
    # if so, we will store the result in the context variable define by the value
    VARIABLE_OUTPUT_KEY = getattr(settings, 'QUERY_PARAMETERS_VARIABLE_OUTPUT_KEY', 'as')
    params, as_var = pluck_property(params, VARIABLE_OUTPUT_KEY)

    # check to see if a special variable input key has been passed (default to `with`); 
    # if so, we will pull the query string from the context variable defined by the value
    VARIABLE_INPUT_KEY = getattr(settings, 'QUERY_PARAMETERS_VARIABLE_INPUT_KEY', 'with')
    params, with_var = pluck_property(params, VARIABLE_INPUT_KEY)

    return QueryStringDeleteNode(params, as_var, with_var)

class QueryStringDeleteNode(template.Node):
    def __init__(self, parameter_delete_list, as_var, with_var):
        self.parameter_delete_list = parameter_delete_list
        self.as_var = as_var
        self.with_var = with_var

    def contextual_parameter_delete_list(self, context):
        """
        Searches the context for any variables named after the provided parameters; if any found,
        replaces the parameter name with the corresponding variable value

        e.g.
        first_property = 'test'
        [first_property,'second_property'] => ['test','second_property']
        """
        parameters = map(lambda key: get_value(key, context), self.parameter_delete_list)
        return parameters

    def render(self, context):
        # if we have been passed a querystring from the context, load it; otherwise, pull from the context
        if self.with_var:
            query_string = get_value(self.with_var, context)
        else:
            query_string = get_query_string(context)

        existing_query_dict = QueryDict(query_string).copy()
        
        for parameter in self.contextual_parameter_delete_list(context):
            if existing_query_dict.get(parameter):
                del existing_query_dict[parameter]

        result = existing_query_dict.urlencode()

        if self.as_var:
            # if we are storing result as a context property, do so and reutrn a blank string
            context[self.as_var] = result
            return ''
        else:
            # ... otherwise return the value
            return result


# HELPER METHDOS
def get_query_string(context):
    """
    Return the query string from the request context
    """
    request = context.get('request', None)
    if request is None:
        return ''
    else:
        return request.GET.urlencode()

def get_value(key, context):
    """
    Return the value of variable `key` from the context if it exists; otherwise, returns the key name
    """
    try:
        value = template.Variable(key)
        value = value.resolve(context)
    except template.VariableDoesNotExist:
        return key
    except template.TemplateSyntaxError:
        return key
    else:
        return value

def pluck_property(params, property_key):
    """
    Searches a list of params for a `property_key=value` match. If one is found, it stores the value and removes from the list of params
    Returns a tuple of (params, value). If no property_key is found, value is None. The returne params will be plucked of the match, if one is found
    """
    for val in list(params):
        match = re.match('%s=(\w+)' % property_key, val)
        if match:
            params.pop(params.index(val))
            return (params, match.group(1))
    return (params, None)



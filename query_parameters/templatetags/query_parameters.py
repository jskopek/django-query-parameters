from django import template
from django.http import QueryDict

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

    try:
        key_value_pairs = token.split_contents()[1:]
        key_value_dict = dict(key_value_pair.split('=') for key_value_pair in key_value_pairs)
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires arguments to be in `key=value` pairs' % token.contents.split()[0])

    return QueryStringSetNode(key_value_dict)

class QueryStringSetNode(template.Node):
    def __init__(self, parameter_dict):
        self._parameter_dict = parameter_dict

    def contextual_parameter_dict(self, context):
        """
        Searches the context for any variables named after the provided parameters; if any found,
        replaces the parameter name with the corresponding variable value

        e.g.
        first_property = 'test'
        {first_property: 'value_1', 'key_2': first_property} => {'test': 'value_1', 'key_2': 'test'}
        """

        value_parameter_dict = {}
        for key, value in self._parameter_dict.items():
            value_parameter_dict[get_value(key,context)] = get_value(value,context)
        return value_parameter_dict

    def render(self, context):
        query_string = get_query_string(context)
        existing_query_dict = QueryDict(query_string).copy()
        for key, value in self.contextual_parameter_dict(context).items():
            existing_query_dict[key] = value
        #existing_query_dict.update(self.contextual_parameter_dict(context))
        return existing_query_dict.urlencode()

# DELETING PARAMETERS
@register.tag
def del_query_parameters(parser, token):
    """
    Takes a 1+ list of keys and generates an updated querystring that removes those keys.

    e.g. querystring = http://localhost/?page=1&limit=20
    {% del_query_parameters page order %} => limit=20
    """

    params = token.split_contents()[1:]
    return QueryStringDeleteNode(params)

class QueryStringDeleteNode(template.Node):
    def __init__(self, parameter_delete_list):
        self._parameter_delete_list = parameter_delete_list

    def contextual_parameter_delete_list(self, context):
        """
        Searches the context for any variables named after the provided parameters; if any found,
        replaces the parameter name with the corresponding variable value

        e.g.
        first_property = 'test'
        [first_property,'second_property'] => ['test','second_property']
        """
        parameters = map(lambda key: get_value(key, context), self._parameter_delete_list)
        return parameters

    def render(self, context):
        query_string = get_query_string(context)
        existing_query_dict = QueryDict(query_string).copy()
        
        for parameter in self.contextual_parameter_delete_list(context):
            if existing_query_dict.get(parameter):
                del existing_query_dict[parameter]
        return existing_query_dict.urlencode()

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
    else:
        return value




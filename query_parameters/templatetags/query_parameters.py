from django import template
from django.http import QueryDict

register = template.Library()

class QueryStringSetNode(template.Node):
    def __init__(self, parameter_dict):
        self.parameter_dict = parameter_dict

    def render(self, context):
        qstring = get_query_string(context)

        value_parameter_dict = {}
        for key, value in self.parameter_dict.items():
            value_parameter_dict[get_value(key,context)] = get_value(value,context)

        existing_query_dict = QueryDict(qstring).copy()
        existing_query_dict.update(value_parameter_dict)
        return existing_query_dict.urlencode()

class QueryStringDeleteNode(template.Node):
    def __init__(self, parameter_delete_list):
        self.parameter_delete_list = parameter_delete_list

    def render(self, context):
        qstring = get_query_string(context)
        existing_query_dict = QueryDict(qstring).copy()
        print existing_query_dict
        
        parameters = map(lambda key: get_value(key, context), self.parameter_delete_list)
        for parameter in parameters:
            if existing_query_dict.get(parameter):
                del existing_query_dict[parameter]
        return existing_query_dict.urlencode()

@register.tag
def set_query_parameters(parser, token):
    try:
        key_value_pairs = token.split_contents()[1:]
        key_value_dict = dict(key_value_pair.split('=') for key_value_pair in key_value_pairs)
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires arguments to be in `key=value` pairs' % token.contents.split()[0])

    print key_value_dict
    return QueryStringSetNode(key_value_dict)

@register.tag
def del_query_parameters(parser, token):
    params = token.split_contents()[1:]
    return QueryStringDeleteNode(params)


# helper methods
def get_query_string(context):
    request = context.get('request', None)
    if request is None:
        return ''
    else:
        return request.GET.urlencode()

def get_value(key, context):
    print 'get_value: %s' % key
    try:
        value = template.Variable(key)
        value = value.resolve(context)
    except template.VariableDoesNotExist:
        return key
    else:
        return value




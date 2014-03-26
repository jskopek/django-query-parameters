from django import template
from django.http import QueryDict

register = template.Library()

class QueryStringSetNode(template.Node):
    def __init__(self, query_dict):
        self.query_dict = query_dict

    def render(self, context):
        qstring = get_query_string(context)

        existing_query_dict = QueryDict(qstring).copy()
        existing_query_dict.update(self.query_dict)
        return existing_query_dict.urlencode()

class QueryStringDeleteNode(template.Node):
    def __init__(self, parameter_delete_list):
        self.parameter_delete_list = parameter_delete_list

    def render(self, context):
        qstring = get_query_string(context)
        existing_query_dict = QueryDict(qstring).copy()
        
        parameters = map(lambda key: get_value(key, context), self.parameter_delete_list)
        for parameter in parameters:
            if existing_query_dict.get(parameter):
                del existing_query_dict[parameter]
        return existing_query_dict.urlencode()

@register.tag
def set_query_parameters(parser, token):
    try:
        tag_name, key, value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires two arguments' % token.contents.split()[0])

    return QueryStringSetNode({'setting':'this'})

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
    try:
        value = template.Variable(key)
        value = value.resolve(context)
    except template.VariableDoesNotExist:
        return key
    else:
        return value




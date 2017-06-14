from operator import itemgetter

from django.contrib.admin.templatetags.admin_list import result_headers, result_hidden_fields, results
from django.template import Library

register = Library()


@register.inclusion_tag("admin/change_list_results_new.html")
def result_list_new(cl):
    """
    Display the headers and data list together.
    """
    headers = list(result_headers(cl))
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'results': list(results(cl))}


@register.inclusion_tag("admin/change_list_results_new_list.html")
def result_list_new_list(cl, data, headers):
    """
    Display the headers and data list together.
    """
    headers_rus = list(map(itemgetter(0), headers))
    headers_lat = list(map(itemgetter(1), headers))
    print([[item.get(key) for key in headers_lat] for item in data])
    return {'cl': cl,
            'result_headers': headers_rus,
            'results': [[item.get(key) for key in headers_lat] for item in data],
            'data': data}

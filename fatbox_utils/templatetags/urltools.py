from django.http import QueryDict
from django import template

from urlparse import urlparse, urlunparse

register = template.Library()

@register.simple_tag(takes_context=True)
def build_absolute_uri(context, relative_url):
    if 'request' not in context:
        return relative_url
    return context['request'].build_absolute_uri(relative_url)

@register.simple_tag(takes_context=True)
def modify_querystring(context, **kwargs):
    if 'request' not in context:
        return 'You need to enable the request context processor!'

    # thanks to: http://stackoverflow.com/a/12423248
    # updated to allow None to delete an element
    url = context['request'].get_full_path()
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    query_dict = QueryDict(query).copy()
    for key in kwargs:
        if kwargs[key] is None:
            if key in query_dict:
                del query_dict[key]
        else:
            query_dict[key] = kwargs[key]
    query = query_dict.urlencode()
    return urlunparse((scheme, netloc, path, params, query, fragment))

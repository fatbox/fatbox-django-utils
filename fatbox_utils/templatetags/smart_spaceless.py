from django.conf import settings
from django import template
from django.utils.html import strip_spaces_between_tags

register = template.Library()

class SmartSpacelessNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        return content if settings.DEBUG else strip_spaces_between_tags(content.strip())

@register.tag
def smart_spaceless(parser, token):
    """
    This template tag will strip all extra space from its contents, but
    only if DEBUG is True in your settings.
    """
    nodelist = parser.parse(('end_smart_spaceless',))
    parser.delete_first_token()
    return SmartSpacelessNode(nodelist)

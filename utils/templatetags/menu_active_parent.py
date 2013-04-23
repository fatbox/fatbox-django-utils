from django import template

register = template.Library()

@register.simple_tag
def active_parent(node):
    """
    Checks to see if our children contain the active page
    """
    def check_active_children(node):
        for child in node.children:
            if child.is_active:
                return True

            ret = check_active_children(child)
            if ret == True:
                return True

    if check_active_children(node):
        return 'active'

    return ''

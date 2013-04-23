import hashlib
from django.core.cache import cache

def delete_template_fragment_cache(fragment_name='', *args):
    """
	Original code from: http://djangosnippets.org/snippets/2723/
	
	Updated by Evan Borgstrom - April 14th, 2013
	 * reformatted
	 * ensure all args are str()
    """
    cache.delete('template.cache.%s.%s' % (
        fragment_name,
        hashlib.md5(u':'.join([
            str(arg)
            for arg in args
        ])).hexdigest()
    ))

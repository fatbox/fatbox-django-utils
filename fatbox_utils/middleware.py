from django.utils import translation

class ManualLanguageMiddleware(object):
    """
    Allow the language to be set based on 'lang' being present in the
    GET or POST data
    """
    def process_request(self, request):
        lang = request.REQUEST.get('lang')
        if lang is not None:
            # don't trust input from users, force string type and only
            # take the first two letters
            translation.activate(str(lang)[0:2])

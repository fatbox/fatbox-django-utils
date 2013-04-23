from django.utils import translation

def current_lang(request):
    return {
        'current_lang': translation.get_language()[0:2],
    }

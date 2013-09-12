from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.conf import settings
from django.db import models

class TranslatableException(Exception):
    pass

class TranslatableModel(models.Model):
    """
    An abstract base model that adds the needed language field with its
    choices set to the active languages in the settings file
    """
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        help_text=_("The language for this translation")
    )

    class Meta:
        abstract = True

class translatable_property(object):
    """
    This works similar to the property built-in by creating a getter for a
    attribute on a model, except that it returns the value from an attr on
    a related model that is fetched based on the current language.
    """

    def __init__(self, name, related):
        """
        When creating a translatable_property you need to pass the name of the
        related attribute as well as the name of the related manage on the
        object you're attaching this to.
        """
        self.name = name
        self.related = related

    def __get__(self, obj, objtype):
        """
        Look up a translatable_property
        """
        # first fetch our related manager
        related_manager = getattr(obj, self.related)
        if not related_manager:
            raise TranslatableException("Object (%s) doesn't have a \"%s\" property" % (
                obj,
                self.related))

        def related_attr(lang):
            """
            Closure to make life easier, it returns the related attr based on
            the provided language.
            """
            # use .all() here because if we have a prefetch_cache the value is there already
            for e in related_manager.all():
                if e.language == lang:
                    try:
                        return getattr(e, self.name)
                    except IndexError:
                        pass

        # first try by asking the translation module for the current language
        # this works via the locale middleware and will return the preferred
        # language from the current request if available, falling back to the
        # default language otherwise.
        # we slice just the first two characters so that both 'en-us' and
        # 'en-ca' will return 'en'.
        current_lang = translation.get_language()[0:2]
        val = related_attr(current_lang)
        if val:
            return val

        # otherwise fall back to our default language
        return related_attr(settings.DEFAULT_LANGUAGE)


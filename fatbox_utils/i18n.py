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
    This works by creating an property on your model that will proxy get, set
    and delete methods to the related translation objects (extending from the
    TranslatableModel class) that match the current language. If an instance
    of a translatable model does not exist for the current language it will
    fall back to the DEFAULT_LANGUAGE, as defined in your settings, for get
    operations only.
    """

    def __init__(self, name, related):
        """
        When creating a translatable_property you need to pass the name of the
        related attribute as well as the name of the related manager on the
        instance you're attaching this to.
        """
        self.name = name
        self.related = related

    def related_model(self, instance, use_default=False):
        """
        Returns the related model for the specified instance
        """
        # fetch our related manager
        related_manager = getattr(instance, self.related)
        if not related_manager:
            raise TranslatableException("Object (%s) doesn't have a \"%s\" property" % (
                instance,
                self.related))

        def _for_lang(lang):
            # use .all() here because if we have a prefetch_cache the value is there already
            for instance in related_manager.all():
                if instance.language == lang:
                    return instance

        # first try the current language
        instance = _for_lang(translation.get_language()[0:2])
        if instance and hasattr(instance, self.name):
            return instance

        if use_default:
            # fall back to the default language
            instance = _for_lang(settings.DEFAULT_LANGUAGE)
            if instance and hasattr(instance, self.name):
                return instance

    def __get__(self, instance, owner):
        """
        Look up a translatable attribute
        """
        related_model = self.related_model(instance, True)
        if related_model:
            return getattr(related_model, self.name)

    def __set__(self, instance, value):
        """
        Set a translatable attribute
        """
        related_model = self.related_model(instance)
        if related_model:
            return setattr(related_model, self.name, value)

    def __del__(self, instance):
        related_model = self.related_model(instance)
        if related_model:
            return delattr(related_model, self.name)

FatBox Django Utils
~~~~~~~~~~~~~~~~~~~

This is a collection of general utilities for Django projects built by FatBox.

Installation
============

Install using pip::

    pip install fatbox-django-utils

These utilities require Django 1.3+. They may work with earlier versions but
haven't been tested.

Rendering templates
===================

render_to decorator
-------------------

The ``render_to`` decorator allows you to very easily render templates from
your view functions. Simply decorate your view function and specify the name
of the template to render to, then return a dict from your view function that
contains variables that will be in the context when rendering the template.

.. code-block:: python

    from fatbox_utils.decorators import render_to

    @render_to('myapp/template.html')
    def myview(request):
        return {
            'var1': var1,
            'var2': var2
        }

You can change the template on the fly by returning a list or tuple where the
first element is the name of the template and the second element is the dict to
use for the context.

.. code-block:: python

    @render_to('myapp/template.html')
        context = {
            'var1': var1,
            'var2': var2
        }

        # if something is true then use our other template
        if something_is_true:
            return ('other_template.html', context)

        # otherwise use the default template
        return context

Lastly if you don't return a dict or a list/tuple then ``render_to`` will just
return what you give it. This ensures that if you return things like
``HttpResponseRedirect`` objects they will work as expected, but also means
that you are free to craft your own response should it be required. Anything
that's valid to return from a standard Django view will work.

Humanize
========

humanize_time function
----------------------

The ``humanize_time`` function summarizes time based on the units you provide
to it. For example here is what is run in the doc tests:

.. code-block:: python

    >>> humanize_time(173, "hours")
    u'1 week, 5 hours'
    >>> humanize_time(17313, "seconds")
    u'4 hours, 48 minutes, 33 seconds'
    >>> humanize_time(5400, "seconds")
    u'1 hour, 30 minutes'
    >>> humanize_time(90, "weeks")
    u'1 year, 10 months, 2 weeks'
    >>> humanize_time(42, "months")
    u'3 years, 6 months'
    >>> humanize_time(500, "days")
    u'1 year, 5 months, 3 weeks, 3 days'

See: http://stackoverflow.com/a/6574789

Cache
=====

delete_template_fragment_cache function
---------------------------------------

This is a function that deletes a named template fragment cache.

See: http://djangosnippets.org/snippets/2723/

In your template:

.. code-block:: html+django

    {% load cache %}

    {% cache 3600 my_cache_block request.user.username %}
    ...
    {% endcache %}

And in your view:

.. code-block:: python

    from fatbox_utils.cache import delete_template_fragment_cache

    def my_view(request):
        ...
        delete_template_fragment_cache("my_cache_block", request.user.username)
        ...

i18n / Translation
==================

This package includes a number of different utilities for managing and working
with i18n / translation in your project.

current_lang context processor
------------------------------

This is a context processor that adds ``current_lang`` to your template context
as a 2 letter language code (ie. ``en``, ``fr``, ``pt``, etc).

Just add ``fatbox_utils.context_processors.current_lang`` to the
``TEMPLATE_CONTEXT_PROCESSORS`` setting.

ManualLanguageMiddleware
------------------------

This is a middleware class that allows you to force the language used by the
Django translation layer based on a querystring parameter.

To use it simply add ``fatbox_utils.middleware.ManualLanguageMiddleware`` to
the ``MIDDLEWARE_CLASSES`` setting. Then you can pass a two character language
code to a get parameter named ``lang`` to activate a specific language.

translatable_property for Models
--------------------------------

Often times when working on a project that deals with multiple languages you
want to have certain properties of a model translatable. The
``translatable_property`` class provides a convenient interface to define your
properties that should be available in multiple languages.

Consider the following example ``models.py`` file:

.. code-block:: python

    from django.db import models
    from fatbox_utils.i18n import translatable_property

    class Event(models.Model):
        start = models.DateTimeField()
        end = models.DateTimeField()

        title = translatable_property('title', 'descriptions')
        details = translatable_property('details', 'descriptions')

    class EventDescription(models.Model):
        event = models.ForeignKey(
            Event,
            related_name='descriptions'
        )
        language = models.CharField(
            max_length=2,
            help_text="The ISO two character language code (en, fr, es, pt, etc)"
        )
        title = models.CharField(
            max_length=32
        )
        details = models.TextField()

What this does is add two models ``Event`` and ``EventDescription`` where the
``EventDescription`` model has a foreign key to ``Event`` and sets up a related
manager named ``descriptions``.

On the ``Event`` model we define two properties using the ``translatable_property``
class. When defining these properties the first argument is the field on the
related model and the second argument is the name of the manager that we can use
to lookup the related model that corresponds to the current language.

When you access one of the ``translatable_property`` properties on your model
it will try to fetch the related object from the ``descriptions`` manager where
the related object has a field named ``language`` that matches the current
language, as defined by the ``get_language`` function from the
``django.utils.translation`` package. If it can't find a related object with a
matching ``language`` field it will then try to get one with the default
language, as defined by ``settings.DEFAULT_LANGUAGE``.

Performance Optimization
````````````````````````

If you don't do any optimization of your querysets once you reach even a modest
number of ``Event`` objects iterating over their querysets can become a HUGE
burden on your database due to the number of SELECT lookups it needs to do when
fetching all of the related ``EventDescription`` objects.

To combat this you can use Django's ``prefetch_related`` queryset function to
fetch all of the related descriptions in one fell swoop, reducing the number of
queries to 2.

.. code-block:: python

    Event.objects.filter(...).prefetch_related('descriptions')


Template Tags
=============

Smart Spaceless
---------------

The Django ``{% spaceless %}`` tag is a great way to optimize your templates
so that you send the smallest amount of data possible to clients, however when
you're in development turning spaceless on makes it hard to read your HTML and
debug problems.

The ``{% smart_spaceless %}`` tag works exactly the same as the normal tag,
except that it only applies spaceless when your ``DEBUG`` setting is ``False``.

.. code-block:: html+django

    {% load smart_spaceless %}{% smart_spaceless %}
    <!doctype html>
    <html>
    ...
    </html>
    {% end_smart_spaceless %}

URL Tools
---------

The URL Tools template tags provide some convenience functions when working
with URLs in your templates. They all require that the ``request`` be available
in the current context so make sure that you have
``django.core.context_processors.request`` enabled in your
``TEMPLATE_CONTEXT_PROCESSORS`` setting.

build_absolute_uri
``````````````````

This exposes the ``build_absolute_uri`` function of the request object to your
templates.

.. code-block:: html+django

    {% load urltools %}

    <a href="{% build_absolute_uri myobject.get_absolute_url %}">Link</a>

modify_querystring
``````````````````

This allows you to modify individual querystring parameters, without needing
to reconstruct the entire URL.

For example, say you're on a page that shows a listing of objects and you have
flags for determining if the user will view the results as a grid or as a list.
On this same view you may accept a querystring parameter to further limit the
query so having to manually reconstruct the URL just to change the format
becomes a much more complex task. With ``modify_querystring`` we can change
just the ``format`` querystring parameter (even adding it if it doesn't exist)
without having to reconstruct anything.

.. code-block:: html+django

    {% load urltools %}

    <div>
      <span>Sort:</span>
      <a href="{% modify_querystring sort="date" %}"{% if sort_by == "date" %} class="active"{% endif %}>By Date</a> |
      <a href="{% modify_querystring sort="title" %}"{% if sort_by == "title" %} class="active"{% endif %}>Alphabetically</a>
    </div>

    <div>
        <span>View as:</span>
        <a href="{% modify_querystring format="list" %}" {% if page_format == "list"%}class="active"{% endif %}>List</a> |
        <a href="{% modify_querystring format="grid" %}" {% if page_format == "grid"%}class="active"{% endif %}>Grid</a>
    </div>

#!/usr/bin/env python

from setuptools import setup

setup(name='fatbox-django-utils',
      packages=['utils'],
      include_package_data=True,
      version="1.0",
      description='A collection of Django utilities, built by FatBox',
      long_description=open('README.rst').read(),
      author='Evan Borgstrom',
      author_email='evan@fatbox.ca',
      url='https://github.com/fatbox/fatbox-django-utils',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      install_requires=['setuptools'])

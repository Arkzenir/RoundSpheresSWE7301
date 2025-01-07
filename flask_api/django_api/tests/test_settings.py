# test_settings.py

"""
Django test settings that override the main settings.py
for testing purposes.
"""

from django_api.settings import *  # Import all settings from main settings file


DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}
DEBUG = False

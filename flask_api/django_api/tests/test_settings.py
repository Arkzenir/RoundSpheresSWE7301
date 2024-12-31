# test_settings.py

"""
Django test settings that override the main settings.py
for testing purposes.
"""

from django_api.settings import *  # Import all settings from main settings file


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Using in-memory SQLite database
    }
}

DEBUG = False

# Disable migrations during tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()
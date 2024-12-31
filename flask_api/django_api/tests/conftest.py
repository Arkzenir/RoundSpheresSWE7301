import pytest
from django.core.management import call_command
from django.conf import settings
from rest_framework.test import APIClient
from django_api.init_django import init

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('migrate')

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
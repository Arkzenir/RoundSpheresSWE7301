import pytest
from django.core.management import call_command

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Ensure database is properly set up for tests"""
    with django_db_blocker.unblock():
        print("migrated")
        call_command('migrate')

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests"""
    pass

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
import os
import django

def init():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api.django_base.settings')
    django.setup()

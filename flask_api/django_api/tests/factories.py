import factory
from django_api.api.models import SciRecord
from datetime import date, time

class SciRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SciRecord

    date = factory.LazyFunction(lambda: date(2024, 1, 1))
    time = factory.LazyFunction(lambda: time(12, 0))
    time_offset = -5
    coordinate = [40.7128, -74.0060]
    air_temperature = 20.5
    humidity = 65.0
    wind_speed = 10.2
    wind_direction = 180.0
    precipitation = 0.0
    haze = 5.0
    water_temperature = 18.5
    notes = factory.Sequence(lambda n: f"Test record {n}")
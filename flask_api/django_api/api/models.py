from django.db import models

# Create your models here.
class Item(models.Model):
    id = models.IntegerField
    date = models.DateField
    time = models.TimeField
    time_offset = models.IntegerField
    coordinate = models.JSONField #Coordinates must be jsonified since arrayfields only work in postgres
    air_tempature = models.FloatField
    humidity = models.FloatField
    wind_speed = models.FloatField
    wind_direction = models.FloatField
    precipitation = models.FloatField
    haze = models.FloatField
    water_tempature = models.FloatField
    notes = models.TextField

def __str__(self):
        return self.id
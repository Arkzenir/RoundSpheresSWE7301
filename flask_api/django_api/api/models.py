from django.db import models

# Create your models here.
class SciRecord(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-increment primary key
    date = models.DateField
    time = models.TimeField
    time_offset = models.IntegerField
    coordinate = models.JSONField #Coordinates must be jsonified since arrayfields only work in postgres
    air_temperature = models.FloatField
    humidity = models.FloatField
    wind_speed = models.FloatField
    wind_direction = models.FloatField
    precipitation = models.FloatField
    haze = models.FloatField
    water_temperature = models.FloatField
    notes = models.TextField(blank=True, null=True)  # Optional field

def __str__(self):
        return f"Record {self.id}"
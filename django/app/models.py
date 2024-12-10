from django.db import models


class membershipModel(models.Model):
    id = models.AutoField(primary_key = True)
    First_name = models.CharField(max_length=255)
    Last_name = models.CharField(max_length=255)
    User_name = models.CharField(max_length=255)
    Email_address = models.CharField(max_length=255)
    Password = models.CharField(max_length=512)
    Date_added = models.DateTimeField(auto_now_add=True)
    image_url = models.ImageField(upload_to='images/', blank=True, null=True)

    class Meta:
        db_table="Membership_tbl"

# Create your models here.

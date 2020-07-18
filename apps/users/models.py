from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from django.db.models.signals import post_save
from django.dispatch import receiver
import random

from django.contrib.postgres.operations import CreateExtension
from django.db import migrations

class Migration(migrations.Migration):

    operations = [
        CreateExtension('postgis'),
    ]

class CustomUser(AbstractUser):
    # is_merchant = models.BooleanField(default=False)
    mobile_number = PhoneNumberField(
        blank=True,
        null = True,
        region='IN'
    )
    profile_picture = models.ImageField(upload_to = 'profile_pictures', null = True)
    bio  = models.CharField(max_length=500, blank=True, null=True)
    user_id = models.BigIntegerField(primary_key=True)
    social_id = models.CharField(unique=True, max_length=32, null=True)

    ACCOUNT_TYPE_CHOICES = (
    ("PUBLIC", "public"),
    ("PRIVATE", "private"),
    
)
    account_type = models.CharField(max_length=7,
                  choices=ACCOUNT_TYPE_CHOICES,
                  default="PRIVATE")
    email_verified = models.BooleanField(default = False)              







    def __str__(self):
        return "{}".format(self.email)

    @property
    def group_name(self):
        """
        Returns a group name based on the user's id to be used by Django Channels.
      
        """
        return "user_%s" % self.user_id

    def save(self, *args, **kwargs):
        while not self.user_id:
            newId = random.randrange(1000000000, 10000000000)

            if not CustomUser.objects.filter(user_id = newId).exists():
                self.user_id = newId


        super().save(*args, **kwargs)



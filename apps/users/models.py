from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import urllib.request

from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import os
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile

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
    profile_picture_url = models.URLField()
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

    def get_remote_image(self):
        if self.profile_picture_url and not self.profile_picture:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.profile_picture_url).read())
            img_temp.flush()
            self.profile_picture.save("image_%s" % str(self.user_id), File(img_temp))

    def save(self, *args, **kwargs):
        while not self.user_id:
            newId = random.randrange(1000000000, 10000000000)

            if not CustomUser.objects.filter(user_id = newId).exists():
                self.user_id = newId

        self.get_remote_image()
        super().save(*args, **kwargs)



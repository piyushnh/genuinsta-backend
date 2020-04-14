from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    # is_merchant = models.BooleanField(default=False)
    mobile_number = PhoneNumberField(
        blank=True,
        null = True,
        region='IN'
    )
    profile_picture = models.ImageField(upload_to = 'profile_pictures', null = True)
    bio  = models.CharField(max_length=500, blank=True, null=True)
    user_id = models.CharField(max_length=500, unique=True, )





    def __str__(self):
        return "{}".format(self.email)



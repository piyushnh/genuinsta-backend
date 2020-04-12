from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    is_merchant = models.BooleanField(default=False)
    mobile_number = PhoneNumberField(
        blank=True,
        null = True,
        region='IN'
    )



    def __str__(self):
        return "{}".format(self.email)



from django.db import models

from django.conf import settings

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class MerchantProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'merchant_profile')

# @receiver(post_save, sender=User)
# def create_merchant_profile(sender, instance, created, **kwargs):
#     if created:
#         MerchantProfile.objects.create(owner=instance)

# @receiver(post_save, sender=User)
# def save_merchant_profile(sender, instance, **kwargs):
#     instance.profile.save()
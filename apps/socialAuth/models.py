try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField


class CredentialsModel(models.Model):
  id = models.ForeignKey(User, primary_key=True, on_delete = models.CASCADE)
  credential = CredentialsField()
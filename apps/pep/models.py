from django.db import models
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from apps.posts.models import *


# Create your models here

#post a pic with your longlost friend from school showing. Ypu ma 

class Pep(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='pep',  )
    title = models.CharField(max_length=30)
    description = models.TextField(null = False)
    example = models.ForeignKey(Post, on_delete=models.DO_NOTHING, related_name='pep_example') 
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    location = models.TextField(null=True)
    is_draft = models.BooleanField(default=False)
    PRIVACY_TYPE_CHOICES = (
    ("FRIENDS", "friends"),
    ("FOLLOWERS", "followers"),
    )
    privacy_type = models.CharField(max_length=20,
                  choices=PRIVACY_TYPE_CHOICES,
                  default="FRIENDS")



    def __str__(self):
        return str(self.id)


    def save(self, *args, **kwargs):
        while not self.id:
            newId = random.randrange(1000000000, 10000000000)

            if not Pep.objects.filter(id = newId).exists():
                self.id = newId

        super().save(*args, **kwargs)

class Tag(models.Model):
    id = models.BigIntegerField(primary_key=True)
    peps = models.ManyToManyField(Pep,related_name='peps',  )
    # user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='hashtags',  )
    cerated_at = models.DateTimeField(auto_now_add=True, null=False)
    content = models.CharField(max_length=20, blank=False, null=False, unique=True)
     

    def __str__(self):
        return str(self.content)

    def save(self, *args, **kwargs):
        while not self.id:
            newId = random.randrange(1000000000, 10000000000)

            if not Tag.objects.filter(id = newId).exists():
                self.id = newId

        super().save(*args, **kwargs)

from django.db import models
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    group_id = models.CharField(primary_key=True, max_length = 15)
    admin = models.ForeignKey(User,on_delete=models.CASCADE,related_name='groups_owned',  )
    description = models.TextField(null = False)
    name = models.CharField(null = False, blank = False, max_length = 50)
    members = models.ManyToManyField(User, related_name = 'groups_part_of')
    GROUP_TYPE_CHOICES = (
    ("PUBLIC", "public"),
    ("PRIVATE", "private"),)
    group_type = models.CharField(max_length=7,
                  choices=GROUP_TYPE_CHOICES,
                  default="PRIVATE")
    created_at = models.DateTimeField(auto_now_add=True, null=False)


    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        while not self.group_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Post.objects.filter(group_id = newId).exists():
                self.group_id = newId

        super().save(*args, **kwargs)



        
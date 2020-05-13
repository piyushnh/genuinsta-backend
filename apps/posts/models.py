from django.db import models
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from apps.groups.models import Group


# Create your models here.

class Post(models.Model):
    post_id = models.CharField(primary_key=True, max_length = 15)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts',  )
    description = models.TextField(null = False)
    imgSrc = models.ImageField(upload_to = 'media/post_pics',blank=False ) 
    post_time = models.DateTimeField(auto_now_add=True, null=False)
    location = models.TextField(null=True)


    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        while not self.post_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Post.objects.filter(post_id = newId).exists():
                self.post_id = newId

        super().save(*args, **kwargs)

class PostTags(models.Model):
    post_tag_id = models.CharField(primary_key=True, max_length = 15)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_tags',  )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_tags',  )
     

    def __str__(self):
        return str(self.post_tag_id)

    def save(self, *args, **kwargs):
        while not self.post_tag_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Post.objects.filter(post_tag_id = newId).exists():
                self.post_tag_id = newId

        super().save(*args, **kwargs)

class ProfileViews(models.Model):
    view_id = models.CharField(primary_key=True, max_length = 15)
    view_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='outgoing_views',)
    view_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='incoming_views',)
    view_time = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return str(self.view_id)

    def save(self, *args, **kwargs):
        while not self.view_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Post.objects.filter(view_id = newId).exists():
                self.view_id = newId

        super().save(*args, **kwargs)

class Recommendation(models.Model):
    recommend_id = models.CharField(primary_key=True, max_length = 15)
    recommend_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='outgoing_recommendatiions',)
    recommend_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='incoming_recommendatiions',)
    recommend_time = models.DateTimeField(auto_now_add=True, null=True)
    recommend_of = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='recommends',  )

    def __str__(self):
        return str(self.view_id)

    def save(self, *args, **kwargs):
        while not self.recommend_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Post.objects.filter(recommend_id = newId).exists():
                self.recommend_id = newId

        super().save(*args, **kwargs)

class Tags(models.Model):
    tag_id = models.CharField(primary_key=True, max_length = 15)
    tag = models.CharField(max_length=255, blank=False, null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tags',  )

    def __str__(self):
        return str(self.view_id)

    def save(self, *args, **kwargs):
        while not self.tag_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Post.objects.filter(tag_id = newId).exists():
                self.tag_id = newId

        super().save(*args, **kwargs)

class HashTag(models.Model):
    hashtag_id = models.CharField(primary_key=True, max_length = 15)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='hashtags',  )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='hashtags',  )
    hashtag_time = models.DateTimeField(auto_now_add=True, null=False)
    hashtag = models.CharField(max_length=1000, blank=False, null=False)
     

    def __str__(self):
        return str(self.post_tag_id)

    def save(self, *args, **kwargs):
        while not self.hashtag_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Post.objects.filter(hashtag_id = newId).exists():
                self.hashtag_id = newId

        super().save(*args, **kwargs)

class Like(models.Model):
    like_id = models.CharField(primary_key=True, max_length = 15)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes',  )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes',  )
    like_time = models.DateTimeField(auto_now_add=True, null=False)
     

    def __str__(self):
        return str(self.post_tag_id)

    def save(self, *args, **kwargs):
        while not self.like_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Post.objects.filter(like_id = newId).exists():
                self.like_id = newId

        super().save(*args, **kwargs)



from django.db import models
import logging
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from stream_django.activity import Activity


from apps.groups.models import Group
from sorl.thumbnail import  get_thumbnail
from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor
import re
import uuid
from guardian.shortcuts import assign_perm

# import signals

# Create your models here.

class Post(models.Model):
    post_id = models.CharField(primary_key=True, max_length = 15)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts',  )
    description = models.TextField(null = False)
    image = fields.ImageField(upload_to='post', dependencies=[
        FileDependency( processor=ImageProcessor(
            format='JPEG', scale={'max_width': 640, 'max_height': 320})),
    ]) 
    post_time = models.DateTimeField(auto_now_add=True, null=False)
    location = models.TextField(null=True)


    def __str__(self):
        return str(self.post_id)

   

    # @property
    # def activity_time(self):
    #     atime = self.post_time
    #     if is_aware(self.post_time):
    #         atime = make_naive(atime, pytz.utc)
    #     return atime


        
    #  def is_liked_or_not(self, userId):
    #     return Like.objects.filter(post = self.post_id, user = userIf).exists()
    # liked_or_not = property(is_liked_or_not)    

    def save(self, *args, **kwargs):
        while not self.post_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Post.objects.filter(post_id = newId).exists():
                self.post_id = newId

        try: 

            post_desc =  self.description
            hashtags = re.findall(r"#(\w+)", post_desc)

            for h in hashtags:
                h = h.lower()
                hashtag, created = HashTag.objects.get_or_create(hashtag = h)
                hashtag.posts.add(self)
        
        
        except Exception as e:
            print(e)

        print(self)


        super().save(*args, **kwargs)
        assign_perm('change_post', self.user, self)


class PostTags(models.Model):
    post_tag_id = models.CharField(primary_key=True, max_length = 15)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_tags',  )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_tags',  )
     

    def __str__(self):
        return str(self.post_tag_id)

    def save(self, *args, **kwargs):
        while not self.post_tag_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not PostTags.objects.filter(post_tag_id = newId).exists():
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

            if not ProfileViews.objects.filter(view_id = newId).exists():
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

            if not Recommendation.objects.filter(recommend_id = newId).exists():
                self.recommend_id = newId

        super().save(*args, **kwargs)

class Tag(models.Model):
    tag_id = models.CharField(primary_key=True, max_length = 15)
    post = models.CharField(max_length=255, blank=False, null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tags',  )
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='tags',  )

    def __str__(self):
        return str(self.view_id)

    def save(self, *args, **kwargs):
        while not self.tag_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Tag.objects.filter(tag_id = newId).exists():
                self.tag_id = newId

        super().save(*args, **kwargs)

class HashTag(models.Model):
    hashtag_id = models.CharField(primary_key=True, max_length = 15)
    posts = models.ManyToManyField(Post,related_name='hashtags',  )
    # user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='hashtags',  )
    hashtag_time = models.DateTimeField(auto_now_add=True, null=False)
    hashtag = models.CharField(max_length=1000, blank=False, null=False, unique=True)
     

    def __str__(self):
        return str(self.hashtag)

    def save(self, *args, **kwargs):
        while not self.hashtag_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not HashTag.objects.filter(hashtag_id = newId).exists():
                self.hashtag_id = newId

        super().save(*args, **kwargs)

class Like(models.Model):
    like_id = models.CharField(primary_key=True, max_length = 15)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes',  )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes',  )
    like_time = models.DateTimeField(auto_now_add=True, null=False)
     

    def __str__(self):
        return str(self.like_id)

   

    def save(self, *args, **kwargs):
        while not self.like_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Like.objects.filter(like_id = newId).exists():
                self.like_id = newId


        super().save(*args, **kwargs)

class Comment(models.Model):
    comment_id = models.CharField(primary_key=True, max_length = 15)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments',  )
    comment_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments',  )
    comment_time = models.DateTimeField(auto_now_add=True, null=False)
    COMMENT_TYPE_CHOICES = (
    ("TEXT", "text"),
    ("IMAGE", "image"),
    ("STICKER", "sticker"),)
    comment_type = models.CharField(max_length=7,
                  choices=COMMENT_TYPE_CHOICES,
                  default="TEXT")
    text = models.TextField(null = True)
    #In case of sticker or image, the url will be in this 
    commentSrc = models.ImageField(upload_to='comment_images_stickers')
     

    def __str__(self):
        return str(self.comment_id)

    def save(self, *args, **kwargs):
        while not self.comment_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Comment.objects.filter(comment_id = newId).exists():
                self.comment_id = newId


        super().save(*args, **kwargs)

class Bookmark(models.Model):
    bookmark_id = models.CharField(primary_key=True, max_length = 15)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='bookmarks',  )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='bookmarks',  )
    bookmark_time = models.DateTimeField(auto_now_add=True, null=False)
     

    def __str__(self):
        return str(self.bookmark_id)

    def save(self, *args, **kwargs):
        while not self.bookmark_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Bookmark.objects.filter(bookmark_id = newId).exists():
                self.bookmark_id = newId


        super().save(*args, **kwargs)






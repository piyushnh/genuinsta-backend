from django.db import models
import sys
import logging
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User



from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from apps.groups.models import Group
from sorl.thumbnail import  get_thumbnail
from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor

import re
import uuid
import pytz
from guardian.shortcuts import assign_perm
from django.utils.timezone import is_aware, make_naive
from .tasks import after_posting_task
# from apps.pep.models import Pep
import random

from stream_framework.verbs import register
from stream_framework.verbs.base import Verb


class PostVerb(Verb):
    id = 5
    infinitive = 'post'
    past_tense = 'posted'

register(PostVerb)

# import signals

# Create your models here.

class Post(models.Model):
    post_id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts',  )
    pep = models.ForeignKey('pep.Pep', related_name='posts', on_delete=models.DO_NOTHING, null=True)
    nominees = models.ManyToManyField(User, related_name='nominees')
    description = models.TextField(null = False)
    image = fields.ImageField(upload_to='post') 
    post_time = models.DateTimeField(auto_now_add=True, null=False)
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
        return str(self.post_id)

    def create_activity(self):
        from stream_framework.activity import Activity
        activity = Activity(
            self.user.user_id,
            PostVerb,
            self.post_id,
            time=make_naive(self.post_time, pytz.utc),
            # extra_context=dict(item_id=self.item_id)
        )
        return activity

   

    # @property
    # def activity_time(self):
    #     atime = self.post_time
    #     if is_aware(self.post_time):
    #         atime = make_naive(atime, pytz.utc)
    #     return atime

    # @property
    # def activity_author_feed(self):
    #     '''
    #     The name of the feed where the activity will be stored; this is normally
    #     used by the manager class to determine if the activity should be stored elsewehere than
    #     settings.USER_FEED
    #     '''
    #     print(self.privacy_type)
    #     if self.privacy_type.lower() == 'friends':
    #         return 'friends'
    #     elif self.privacy_type.lower() == 'followers':
    #         return 'followers'
    #     else:
    #         pass


    # def is_liked_or_not(self):
    #     return Like.objects.filter(post = self.post_id, user = self.user).exists()
    # liked_or_not = property(is_liked_or_not)   

    # def is_bookmarked_or_not(self):
    #     return Bookmark.objects.filter(post = self.post_id, user = self.user).exists()
    # bookmarked_or_not = property(is_bookmarked_or_not)    

    def save(self, *args, **kwargs):
        while not self.post_id:
            newId = random.randrange(1000000000, 10000000000)

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



        super().save(*args, **kwargs)


class PostTags(models.Model):
    post_tag_id = models.BigIntegerField(primary_key=True)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_tags',  )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_tags',  )
     

    def __str__(self):
        return str(self.post_tag_id)

    def save(self, *args, **kwargs):
        while not self.post_tag_id:
            newId = random.randrange(1000000000, 10000000000)

            if not PostTags.objects.filter(post_tag_id = newId).exists():
                self.post_tag_id = newId

        super().save(*args, **kwargs)

class ProfileViews(models.Model):
    view_id = models.BigIntegerField(primary_key=True)
    view_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='outgoing_views',)
    view_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='incoming_views',)
    view_time = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return str(self.view_id)

    def save(self, *args, **kwargs):
        while not self.view_id:
            newId = random.randrange(1000000000, 10000000000)

            if not ProfileViews.objects.filter(view_id = newId).exists():
                self.view_id = newId

        super().save(*args, **kwargs)

class Recommendation(models.Model):
    recommend_id = models.BigIntegerField(primary_key=True)
    recommend_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='outgoing_recommendatiions',)
    recommend_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='incoming_recommendatiions',)
    recommend_time = models.DateTimeField(auto_now_add=True, null=True)
    recommend_of = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='recommends',  )

    def __str__(self):
        return str(self.view_id)

    def save(self, *args, **kwargs):
        while not self.recommend_id:
            newId = random.randrange(1000000000, 10000000000)

            if not Recommendation.objects.filter(recommend_id = newId).exists():
                self.recommend_id = newId

        super().save(*args, **kwargs)

class Tag(models.Model):
    tag_id = models.BigIntegerField(primary_key=True)
    post = models.CharField(max_length=255, blank=False, null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tags',  )
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='tags',  )

    def __str__(self):
        return str(self.view_id)

    def save(self, *args, **kwargs):
        while not self.tag_id:
            newId = random.randrange(1000000000, 10000000000)

            if not Tag.objects.filter(tag_id = newId).exists():
                self.tag_id = newId

        super().save(*args, **kwargs)

class HashTag(models.Model):
    hashtag_id = models.BigIntegerField(primary_key=True)
    posts = models.ManyToManyField(Post,related_name='hashtags',  )
    # user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='hashtags',  )
    hashtag_time = models.DateTimeField(auto_now_add=True, null=False)
    hashtag = models.CharField(max_length=1000, blank=False, null=False, unique=True)
     

    def __str__(self):
        return str(self.hashtag)

    def save(self, *args, **kwargs):
        while not self.hashtag_id:
            newId = random.randrange(1000000000, 10000000000)

            if not HashTag.objects.filter(hashtag_id = newId).exists():
                self.hashtag_id = newId

        super().save(*args, **kwargs)

class Like(models.Model):
    like_id = models.BigIntegerField(primary_key=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes',  )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes',  )
    like_time = models.DateTimeField(auto_now_add=True, null=False)
     

    def __str__(self):
        return str(self.like_id)

   

    def save(self, *args, **kwargs):
        while not self.like_id:
            newId = random.randrange(1000000000, 10000000000)

            if not Like.objects.filter(like_id = newId).exists():
                self.like_id = newId


        super().save(*args, **kwargs)

class Comment(models.Model):
    comment_id = models.BigIntegerField(primary_key=True)
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
            newId = random.randrange(1000000000, 10000000000)

            if not Comment.objects.filter(comment_id = newId).exists():
                self.comment_id = newId


        super().save(*args, **kwargs)

class Bookmark(models.Model):
    bookmark_id = models.BigIntegerField(primary_key=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='bookmarks',  )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='bookmarks',  )
    bookmark_time = models.DateTimeField(auto_now_add=True, null=False)
     

    def __str__(self):
        return str(self.bookmark_id)

    def save(self, *args, **kwargs):
        while not self.bookmark_id:
            newId = random.randrange(1000000000, 10000000000)

            if not Bookmark.objects.filter(bookmark_id = newId).exists():
                self.bookmark_id = newId


        super().save(*args, **kwargs)

@receiver(post_save, sender=Comment)
def comment_handler(sender, instance, **kwargs):
        comment = instance
        
        assign_perm('posts.delete_comment', comment.comment_by, comment)
        assign_perm('posts.delete_comment', comment.post.user, comment)
        assign_perm('posts.change_comment', comment.comment_by, comment)

        

@receiver(post_save, sender=Post)
def post_handler(sender, instance, **kwargs):
        post = instance
        # assign_perm('posts.change_comment', post.user, post)
        assign_perm('posts.delete_post', post.user, post)
        if not post.is_draft:
            after_posting_task.delay(post)
            
            

@receiver(post_delete, sender=Post)
def post_delete_handler(sender, instance, **kwargs):
        post = instance
        followFeedManager.remove_post(post)
        friendFeedManager.remove_post(post)
        






    







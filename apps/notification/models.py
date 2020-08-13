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

import uuid
from guardian.shortcuts import assign_perm
from django.utils.timezone import is_aware, make_naive
# from apps.pep.models import Pep
import random
import pytz
from django.db.models.signals import post_save, post_delete
# from .tasks import notify_task

from stream_framework.verbs import register
from stream_framework.verbs.base import Verb


class FollowVerb(Verb):
    id = 6
    infinitive = 'follow'
    past_tense = 'followed'

class FriendRequestVerb(Verb):
    id = 7
    infinitive = 'send_friend_request'
    past_tense = 'friend_request_sent'

class AcceptFriendVerb(Verb):
    id = 8
    infinitive = 'accept_friend_request'
    past_tense = 'friend_request_accepted'

class CommentVerb(Verb):
    id = 9
    infinitive = 'comment'
    past_tense = 'commented'

class NominateVerb(Verb):
    id = 10
    infinitive = 'nominate'
    past_tense = 'nominated'

class TagVerb(Verb):
    id = 11
    infinitive = 'tag'
    past_tense = 'tagged'

class RecommendVerb(Verb):
    id = 12
    infinitive = 'recommend'
    past_tense = 'recommended'


register(FollowVerb)
register(FriendRequestVerb)
register(AcceptFriendVerb)
register(CommentVerb)
register(NominateVerb)
register(TagVerb)
register(RecommendVerb)

getVerbDict = {
    'FRIEND_REQUEST_SENT': FriendRequestVerb,
    'FOLLOWED': FollowVerb,
    'FRIEND_REQUEST_ACCEPTED': AcceptFriendVerb,
    'COMMENTED': CommentVerb,
    'NOMINATED': NominateVerb,
    'RECOMMENDED': RecommendVerb,
    'TAGGED': TagVerb,
}



class Notification(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_notifs',  )
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    CATEGORY_CHOICES = (
    ("FRIEND_REQUEST_SENT", "friend_request_sent"),
    ("FOLLOWING", "following"),
    ("FRIEND_REQUEST_ACCEPTED", "friend_request_accepted"),
    ("COMMENTED", "commented"),
    ("NOMINATED", "nominated"),
    ("RECOMMENDED", "recommended"),
    ("TAGGED", "tagged"),
    )
    category = models.CharField(max_length=20,
                  choices=CATEGORY_CHOICES,
                  )  

    TYPE_CHOICES = (
    ("NOTIFICATION", "notification"),
    ("DATA_MSG", "data_msg"),
    )
    type = models.CharField(max_length=20,
                  choices=TYPE_CHOICES,
                  default='NOTIFICATION'
                  )
    recipient = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='received_notifs',  )
    



    def __str__(self):
        return str(self.id)

    def create_activity(self):
        from stream_framework.activity import Activity
        # from .verbs import NotificationVerb
        
        activity = Activity(
            self.user.user_id,
            getVerbDict[self.category],
            self.id,
            self.recipient.user_id,
            time=make_naive(self.created_at, pytz.utc),
            # extra_context=dict(item_id=self.item_id)
        )
        return activity

 

    def save(self, *args, **kwargs):
        while not self.id:
            newId = random.randrange(1000000000, 10000000000)

            if not Notification.objects.filter(id = newId).exists():
                self.id = newId
        
        super().save(*args, **kwargs)

# @receiver(post_save, sender=Notification)
# def notif_handler(sender, instance, **kwargs):
#         notif = instance
#         # assign_perm('posts.change_comment', post.user, post)
#         # assign_perm('notification.delete_notification', notif.recipient, notif)
#         # if notif.type.lower() == 'notification':
#         notify_task.delay(notif)


from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from django.core.exceptions import ValidationError
import uuid

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from django.dispatch import Signal
from django.dispatch import receiver
from stream_framework.feed_managers.base import FanoutPriority
import random

from .exceptions import AlreadyExistsError, AlreadyFriendsError
from .signals import (
    friendship_request_created, friendship_request_rejected,
    friendship_request_canceled,
    friendship_request_viewed, friendship_request_accepted,
    friendship_removed, follower_created, follower_removed,
    followee_created, followee_removed, following_created, following_removed
)

# from .tasks import (after_following_task, after_unfollowing_task, after_friending_task,
#                    after_unfriending_task)
def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None  

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# implement your feed with redis as storage

from stream_framework.feeds.redis import RedisFeed
from stream_framework.feed_managers.base import Manager

# from .models import Friend, Follow, FriendshipRequest

class TimelineFeed(RedisFeed):
    key_format = 'feed:timeline:%(user_id)s'

class FollowersFeed(RedisFeed):
    key_format = 'feed:followers:%(user_id)s'

class FriendsFeed(RedisFeed):
    key_format = 'feed:friends:%(user_id)s'

class UserFeed(RedisFeed):
    key_format = 'feed:user:%(user_id)s'



class FriendsFeedManager(Manager):
    follow_activity_limit = 50

    feed_classes = dict(
        timeline=TimelineFeed,
    )
    user_feed_class = FriendsFeed
    def add_post(self, post):
        activity = post.create_activity()
        # add user activity adds it to the user feed, and starts the fanout
        self.add_user_activity(post.user.user_id, activity)

    def remove_post(self, post):
        activity = post.create_activity()
        # removes the post from the user's followers feeds
        self.remove_user_activity(post.user.user_id, activity)


    def get_user_follower_ids(self, user_id):
        from itertools import chain
        ids1 = Friend.objects.filter(from_user=user_id).values_list('to_user__user_id', flat=True)
        ids2 = Friend.objects.filter(to_user=user_id).values_list('from_user__user_id', flat=True)
        ids = list(chain(ids1, ids2))
        return {FanoutPriority.HIGH:ids}

friendFeedManager = FriendsFeedManager()

class FollowersFeedManager(Manager):

    follow_activity_limit = 50

    feed_classes = dict(
        timeline=TimelineFeed,
        # friends = FriendsFeed
    )
    user_feed_class = FollowersFeed
    def add_post(self, post):
        activity = post.create_activity()
        # add user activity adds it to the user feed, and starts the fanout
        self.add_user_activity(post.user.user_id, activity)

    def remove_post(self, post):
        activity = post.create_activity()
        # removes the post from the user's followers feeds
        self.remove_user_activity(post.user.user_id, activity)

    def get_user_follower_ids(self, user_id):
        ids = Follow.objects.filter(followee=user_id).values_list('follower__user_id', flat=True)
        return {FanoutPriority.HIGH:ids}

followFeedManager = FollowersFeedManager()


from celery.decorators import task
from celery.utils.log import get_task_logger
import time
from apps.notification.models import Notification



logger = get_task_logger(__name__)


@task(name="after_following_task")
def after_following_task(follower_id, followee_id):
    """To be executed when a user follows someone"""
    try:
        # time.wait(20)

        followee_feed = FollowersFeed(followee_id)
        follower_timeline = TimelineFeed(follower_id)


        # follower_timeline.follow(followee_feed.slug, followee_feed.user_id) 
        followFeedManager.follow_feed(follower_timeline, followee_feed) 



        return 'Done'

    except Exception as e:
        print(e)

@task(name="after_unfollowing_task")
def after_unfollowing_task(follower_id, followee_id):
    """To be executed when a user unfollows someone"""
    try:
        followee_feed = FollowersFeed(followee_id)
        follower_timeline = TimelineFeed(follower_id)

        # follower_timeline.follow(followee_feed.slug, followee_feed.user_id) 
        followFeedManager.unfollow_feed(follower_timeline, followee_feed) 

        return 'Done'

    except Exception as e:
        print(e)

@task(name="after_friending_task")
def after_friending_task(from_user_id, to_user_id):
    """To be executed when a user friends someone"""
    try:
        # time.wait(20)

        followee_feed = FollowersFeed(to_user_id)
        friends_feed = FriendsFeed(to_user_id)

        follower_timeline = TimelineFeed(from_user_id)

        followFeedManager.follow_feed(follower_timeline, followee_feed) 
        friendFeedManager.follow_feed(follower_timeline, friends_feed) 
       


        logger.info("Done")

        return 'Done'

    except Exception as e:
        print(e)

@task(name="after_unfriending_task")
def after_unfriending_task(from_user_id, to_user_id):
    """To be executed when a user unfriends someone"""
    try:
        followee_feed = FollowersFeed(to_user_id)
        friends_feed = FriendsFeed(to_user_id)

        follower_timeline = TimelineFeed(from_user_id)

        followFeedManager.unfollow_feed(follower_timeline, followee_feed) 
        friendFeedManager.unfollow_feed(follower_timeline, friends_feed) 

        return 'Done'

    except Exception as e:
        print(e)




CACHE_TYPES = {
    'friends': 'f-%s',
    'followers': 'fo-%s',
    'following': 'fl-%s',
    'requests': 'fr-%s',
    'sent_requests': 'sfr-%s',
    'unread_requests': 'fru-%s',
    'unread_request_count': 'fruc-%s',
    'read_requests': 'frr-%s',
    'rejected_requests': 'frj-%s',
    'unrejected_requests': 'frur-%s',
    'unrejected_request_count': 'frurc-%s',
}

BUST_CACHES = {
    'friends': ['friends'],
    'followers': ['followers'],
    'following': ['following'],
    'requests': [
        'requests',
        'unread_requests',
        'unread_request_count',
        'read_requests',
        'rejected_requests',
        'unrejected_requests',
        'unrejected_request_count',
    ],
    'sent_requests': ['sent_requests'],
}


def cache_key(type, user_pk):
    """
    Build the cache key for a particular type of cached value
    """
    return CACHE_TYPES[type] % user_pk


def bust_cache(type, user_pk):
    """
    Bust our cache for a given type, can bust multiple caches
    """
    bust_keys = BUST_CACHES[type]
    keys = [CACHE_TYPES[k] % user_pk for k in bust_keys]
    cache.delete_many(keys)




@python_2_unicode_compatible
class FriendshipRequest(models.Model):
    """ Model to represent friendship requests """
    from_user = models.ForeignKey(AUTH_USER_MODEL, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(AUTH_USER_MODEL, related_name='friendship_requests_received', on_delete=models.CASCADE)

    message = models.TextField(_('Message'), blank=True)

    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)
    id = models.BigIntegerField(primary_key = True)


    class Meta:
        verbose_name = _('Friendship Request')
        verbose_name_plural = _('Friendship Requests')
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "User #%s friendship requested #%s" % (self.from_user_id, self.to_user_id)

    def save(self, *args, **kwargs):
        while not self.id:
            newId = random.randrange(1000000000, 10000000000)

            if not Follow.objects.filter(id = newId).exists():
                self.id = newId

        super().save(*args, **kwargs)

    def accept(self):
        """ Accept this friendship request """
        relation1 = Friend.objects.create(
            from_user=self.from_user,
            to_user=self.to_user
        )

        after_friending_task.delay(from_user_id=self.from_user.user_id,
                         to_user_id = self.to_user.user_id)
        
        relation2 = Friend.objects.create(
            from_user=self.to_user,
            to_user=self.from_user
        )

        after_friending_task.delay(from_user=self.to_user,
                         to_user = self.from_user)


        # friendship_request_accepted.send(
        #     sender=self,
        #     from_user=self.from_user,
        #     to_user=self.to_user
        # )


        self.delete()

        # Delete any reverse requests
        FriendshipRequest.objects.filter(
            from_user=self.to_user,
            to_user=self.from_user
        ).delete()

        # Bust requests cache - request is deleted
        bust_cache('requests', self.to_user.pk)
        bust_cache('sent_requests', self.from_user.pk)
        # Bust reverse requests cache - reverse request might be deleted
        bust_cache('requests', self.from_user.pk)
        bust_cache('sent_requests', self.to_user.pk)
        # Bust friends cache - new friends added
        bust_cache('friends', self.to_user.pk)
        bust_cache('friends', self.from_user.pk)

        return True

    def reject(self):
        """ reject this friendship request """
        self.rejected = timezone.now()
        self.save()
        friendship_request_rejected.send(sender=self)
        bust_cache('requests', self.to_user.pk)

    def cancel(self):
        """ cancel this friendship request """
        self.delete()
        friendship_request_canceled.send(sender=self)
        bust_cache('requests', self.to_user.pk)
        bust_cache('sent_requests', self.from_user.pk)
        return True
    

    def mark_viewed(self):
        self.viewed = timezone.now()
        friendship_request_viewed.send(sender=self)
        self.save()
        bust_cache('requests', self.to_user.pk)
        return True


class FriendshipManager(models.Manager):
    """ Friendship manager """

    def friends(self, user):
        """ Return a list of all friends """
        key = cache_key('friends', user.pk)
        friends = cache.get(key)

        if friends is None:
            qs = Friend.objects.select_related('from_user', 'to_user').filter(to_user=user).all()
            friends = [u.from_user for u in qs]
            cache.set(key, friends)

        return friends

    def requests(self, user):
        """ Return a list of friendship requests """
        key = cache_key('requests', user.pk)
        requests = cache.get(key)

        if requests is None:
            qs = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
                to_user=user).all()
            requests = list(qs)
            cache.set(key, requests)

        return requests

    def cancel_request(self, from_user,to_user):
        """ cancel this friendship request """
        relation= FriendshipRequest.objects.get(from_user=from_user,
                        to_user=to_user)
        relation.delete()
        # friendship_request_canceled.send(sender=relation)
        bust_cache('requests', relation.to_user.pk)
        bust_cache('sent_requests', relation.from_user.pk)
        return True

    def sent_requests(self, user):
        """ Return a list of friendship requests from user """
        key = cache_key('sent_requests', user.pk)
        requests = cache.get(key)

        if requests is None:
            qs = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
                from_user=user).all()
            requests = list(qs)
            cache.set(key, requests)

        return requests

    def unread_requests(self, user):
        """ Return a list of unread friendship requests """
        key = cache_key('unread_requests', user.pk)
        unread_requests = cache.get(key)

        if unread_requests is None:
            qs = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
                to_user=user,
                viewed__isnull=True).all()
            unread_requests = list(qs)
            cache.set(key, unread_requests)

        return unread_requests

    def unread_request_count(self, user):
        """ Return a count of unread friendship requests """
        key = cache_key('unread_request_count', user.pk)
        count = cache.get(key)

        if count is None:
            count = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
                to_user=user,
                viewed__isnull=True).count()
            cache.set(key, count)

        return count

    def read_requests(self, user):
        """ Return a list of read friendship requests """
        key = cache_key('read_requests', user.pk)
        read_requests = cache.get(key)

        if read_requests is None:
            qs = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
                to_user=user,
                viewed__isnull=False).all()
            read_requests = list(qs)
            cache.set(key, read_requests)

        return read_requests

    def rejected_requests(self, user):
        """ Return a list of rejected friendship requests """
        key = cache_key('rejected_requests', user.pk)
        rejected_requests = cache.get(key)

        if rejected_requests is None:
            qs = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
                to_user=user,
                rejected__isnull=False).all()
            rejected_requests = list(qs)
            cache.set(key, rejected_requests)

        return rejected_requests

    def unrejected_requests(self, user):
        """ All requests that haven't been rejected """
        key = cache_key('unrejected_requests', user.pk)
        unrejected_requests = cache.get(key)

        if unrejected_requests is None:
            qs = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
                to_user=user,
                rejected__isnull=True).all()
            unrejected_requests = list(qs)
            cache.set(key, unrejected_requests)

        return unrejected_requests

    def unrejected_request_count(self, user):
        """ Return a count of unrejected friendship requests """
        key = cache_key('unrejected_request_count', user.pk)
        count = cache.get(key)

        if count is None:
            count = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(
                to_user=user,
                rejected__isnull=True).count()
            cache.set(key, count)

        return count

    def add_friend(self, from_user, to_user, message=None):
        """ Create a friendship request """
        if from_user == to_user:
            raise ValidationError("Users cannot be friends with themselves")

        if self.are_friends(from_user, to_user):
            raise AlreadyFriendsError("Users are already friends")

        if message is None:
            message = ''

        request, created = FriendshipRequest.objects.get_or_create(
            from_user=from_user,
            to_user=to_user,
        )

        if created is False:
            raise AlreadyExistsError("Friendship already requested")

        if message:
            request.message = message
            request.save()

        bust_cache('requests', to_user.pk)
        bust_cache('sent_requests', from_user.pk)
        # friendship_request_created.send(sender=request)

        return request

    def remove_friend(self, from_user, to_user):
        """ Destroy a friendship relationship """
        try:
            qs = Friend.objects.filter(
                Q(to_user=to_user, from_user=from_user) |
                Q(to_user=from_user, from_user=to_user)
            ).distinct().all()

            if qs:
                # friendship_removed.send(
                #     sender=qs[0],
                #     from_user=from_user,
                #     to_user=to_user
                # )
                after_unfriending_task.delay(from_user.user_id, to_user.user_id)
                after_unfriending_task.delay(to_user.user_id, from_user.user_id)
                qs.delete()
                bust_cache('friends', to_user.pk)
                bust_cache('friends', from_user.pk)
                return True
            else:
                return False
        except Friend.DoesNotExist:
            return False

    def are_friends(self, user1, user2):
        """ Are these two users friends? """
        friends1 = cache.get(cache_key('friends', user1.pk))
        friends2 = cache.get(cache_key('friends', user2.pk))
        if friends1 and user2 in friends1:
            return True
        elif friends2 and user1 in friends2:
            return True
        else:
            try:
                Friend.objects.get(
                to_user=user1, from_user=user2
            )
                return True
            except Friend.DoesNotExist:
                return False

    def friendship_status(self, this_user, other_user):

        if this_user == other_user:
            return 'NONE'

        isFriendRequestSent = get_object_or_none(FriendshipRequest, from_user = this_user, to_user = other_user)
        isFriendRequestReceived = get_object_or_none(FriendshipRequest, from_user = other_user, to_user = this_user)
        
        if (not isFriendRequestSent) and (not isFriendRequestReceived):
            areFriends = Friend.objects.are_friends(this_user, other_user)  
        
        if isFriendRequestSent:
            return 'REQUEST_SENT'
        elif isFriendRequestReceived:
            return 'REQUEST_RECEIVED'
        elif areFriends:
            return 'ARE_FRIENDS'
        else:
            return 'NONE'



@python_2_unicode_compatible
class Friend(models.Model):
    """ Model to represent Friendships """
    to_user = models.ForeignKey(AUTH_USER_MODEL, related_name='friends', on_delete=models.CASCADE)
    from_user = models.ForeignKey(AUTH_USER_MODEL, related_name='_unused_friend_relation', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    id = models.BigIntegerField(primary_key = True)

    objects = FriendshipManager()

    class Meta:
        verbose_name = _('Friend')
        verbose_name_plural = _('Friends')
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "User #%s is friends with #%s" % (self.to_user_id, self.from_user_id)

    def save(self, *args, **kwargs):
        while not self.id:
            newId = random.randrange(1000000000, 10000000000)

            if not Follow.objects.filter(id = newId).exists():
                self.id = newId

        # Ensure users can't be friends with themselves
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super(Friend, self).save(*args, **kwargs)


class FollowingManager(models.Manager):
    """ Following manager """

    def followers(self, user):
        """ Return a list of all followers """
        key = cache_key('followers', user.pk)
        followers = cache.get(key)

        if followers is None:
            qs = Follow.objects.filter(followee=user).all()
            followers = [u.follower for u in qs]
            cache.set(key, followers)

        return followers

    def following(self, user):
        """ Return a list of all users the given user follows """
        key = cache_key('following', user.pk)
        following = cache.get(key)

        if following is None:
            qs = Follow.objects.filter(follower=user).all()
            following = [u.followee for u in qs]
            cache.set(key, following)

        return following

    def add_follower(self, follower, followee):
        """ Create 'follower' follows 'followee' relationship """
        if follower == followee:
            raise ValidationError("Users cannot follow themselves")

        relation, created = Follow.objects.get_or_create(follower=follower, followee=followee)

        if created is False:
            raise AlreadyExistsError("User '%s' already follows '%s'" % (follower, followee))

        # follower_created.send_robust(sender=self, follower=follower)
        # followee_created.send_robust(sender=self, followee=followee)
        # following_created.send_robust(sender=self, following=relation)
        after_following_task.delay(follower.user_id, followee.user_id)


        

        bust_cache('followers', followee.pk)
        bust_cache('following', follower.pk)

        return relation

    def remove_follower(self, follower, followee):
        """ Remove 'follower' follows 'followee' relationship """
        try:
            rel = Follow.objects.get(follower=follower, followee=followee)
            # follower_removed.send(sender=rel, follower=rel.follower)
            # followee_removed.send(sender=rel, followee=rel.followee)
            # following_removed.send(sender=rel, following=rel)

            after_unfollowing_task.delay(follower.user_id, followee.user_id)
            rel.delete()
            bust_cache('followers', followee.pk)
            bust_cache('following', follower.pk)
            return True
        except Follow.DoesNotExist:
            return False

    def follows(self, follower, followee):
        """ Does follower follow followee? Smartly uses caches if exists """
        followers = cache.get(cache_key('following', follower.pk))
        following = cache.get(cache_key('followers', followee.pk))

        if follower == followee:
            return False
        if followers and followee in followers:
            return True
        elif following and follower in following:
            return True
        else:
            try:
                Follow.objects.get(follower=follower, followee=followee)
                return True
            except Follow.DoesNotExist:
                return False




@python_2_unicode_compatible
class Follow(models.Model):
    """ Model to represent Circles """
    id = models.BigIntegerField(primary_key=True)
    follower = models.ForeignKey(AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    objects = FollowingManager()

    class Meta:
        verbose_name = _('Following Relationship')
        verbose_name_plural = _('Following Relationships')
        unique_together = ('follower', 'followee')

    def __str__(self):
        return "User #%s follows #%s" % (self.follower_id, self.followee_id)

    def save(self, *args, **kwargs):
        while not self.id:
            newId = random.randrange(1000000000, 10000000000)

            if not Follow.objects.filter(id = newId).exists():
                self.id = newId
        # Ensure users can't be friends with themselves
        if self.follower == self.followee:
            raise ValidationError("Users cannot follow themselves.")
        super(Follow, self).save(*args, **kwargs)


   

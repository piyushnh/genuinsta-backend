# implement your feed with redis as storage

from stream_framework.feeds.redis import RedisFeed
from stream_framework.feed_managers.base import Manager

from .models import Friend, Follow, FriendshipRequest

class TimelineFeed(RedisFeed):
    key_format = 'feed:timeline:%(user_id)s'

class FollowersFeed(RedisFeed):
    key_format = 'feed:followers:%(user_id)s'

class FriendsFeed(RedisFeed):
    key_format = 'feed:friends:%(user_id)s'

class UserFeed(RedisFeed):
    key_format = 'feed:user:%(user_id)s'



# class FriendsFeedManager(Manager):
#     feed_classes = dict(
#         friends=FriendsFeed,
#     )
#     user_feed_class = UserFeed
#     def add_post(self, post):
#         activity = post.create_activity()
#         # add user activity adds it to the user feed, and starts the fanout
#         self.add_user_activity(post.user.user_id, activity)

#     def get_user_follower_ids(self, user_id):
#         ids = Friend.objects.filter((
#                 Q(from_user=user_id) |
#                 Q(to_user=user_id)
#             )).values_list('user_id', flat=True)
#         return {FanoutPriority.HIGH:ids}

# friendFeedManager = FriendsFeedManager()

# class FollowersFeedManager(Manager):
#     feed_classes = dict(
#         followers=FollowersFeed,
#         # friends = FriendsFeed
#     )
#     user_feed_class = UserFeed
#     def add_post(self, post):
#         activity = post.create_activity()
#         # add user activity adds it to the user feed, and starts the fanout
#         self.add_user_activity(post.user.user_id, activity)

#     def get_user_follower_ids(self, user_id):
#         ids = Follow.objects.filter(followee=user_id).values_list('user_id', flat=True)
#         return {FanoutPriority.HIGH:ids}

# followFeedManager = FollowersFeedManager()

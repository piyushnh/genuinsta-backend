# from stream_framework.feeds.notification_feed.customFeed import CustomNotificationFeed
from stream_framework.feeds.notification_feed.redis import RedisNotificationFeed
# from stream_framework.feeds.aggregated_feed.notification_feed import RedisNotificationFeed
from stream_framework.aggregators.base import RecentRankMixin, BaseAggregator
from django.apps import apps
from .serializers import AggregatedActivitySerializer
from copy import deepcopy
#To integrate channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()
from .models import FriendRequestVerb


# class NominateVerb(Verb):
#     id = 10
#     infinitive = 'nominate'
#     past_tense = 'nominated'

class NotificationAggregator(RecentRankMixin, BaseAggregator):
    
    '''
    Aggregates based on the same verb and same time period
    '''

    def get_group(self, activity):
        '''
        Returns a group based on the day and verb
        '''
        verb_id = activity.verb.id
        date = activity.time.date()
        item_id = activity.extra_context['item_id']

        if verb_id == 9 :

            CommentModel = apps.get_model('posts', 'Comment')
            comment = CommentModel.objects.get(comment_id = item_id)
            post_id = comment.post
            group = '%s-%s-%s' % (verb_id, post_id, date)
        elif verb_id == 11 or verb_id == 12 or verb_id == 13:
            group = '%s-%s-%s' % (verb_id, item_id, date)
        else:
            group = '%s-%s' % (verb_id,  date)
        return group

class MyNotificationFeed(RedisNotificationFeed):
    # : they key format determines where the data gets stored
    key_format = 'feed:notification:%(user_id)s'

    # : the aggregator controls how the activities get aggregated
    aggregator_class = NotificationAggregator

class NotificationManager(object):
    '''
    Abstract the access to the notification feed
    '''
    def add_notif(self, notif):
        feed = MyNotificationFeed(notif.recipient_id)
        activity = notif.create_activity()
        # print(activity.__dict__)
        # print(activity)
        feed.add(activity)
        # print(activity.serialization_id)
        finalActivity = feed[0][0]
        serialized = AggregatedActivitySerializer(finalActivity, context={'user':notif.user})
        print(serialized.data)
        async_to_sync(channel_layer.group_send)(notif.recipient.group_name, {"type": "notify", 'request_data': serialized.data})


notifManager = NotificationManager()
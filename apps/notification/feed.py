# from stream_framework.feeds.notification_feed.customFeed import CustomNotificationFeed
from stream_framework.feeds.notification_feed.redis import RedisNotificationFeed
# from stream_framework.feeds.aggregated_feed.notification_feed import RedisNotificationFeed
from stream_framework.aggregators.base import RecentVerbAggregator

# class NotificationAggregator(BaseAggregator):
#     '''
#     Aggregates based on the same verb and same time period
#     '''
#     def get_group(self, activity):
#         '''
#         Returns a group based on the day and verb
#         '''
#         verb = activity.verb.id
#         date = activity.time.date()
#         group = '%s-%s' % (verb, date)
#         return group

class MyNotificationFeed(RedisNotificationFeed):
    # : they key format determines where the data gets stored
    key_format = 'feed:notification:%(user_id)s'

    # : the aggregator controls how the activities get aggregated
    aggregator_class = RecentVerbAggregator

class NotificationManager(object):
    '''
    Abstract the access to the notification feed
    '''
    def add_notif(self, notif):
        feed = MyNotificationFeed(notif.recipient.user_id)
        activity = notif.create_activity()
        feed.add(activity)

notifManager = NotificationManager()
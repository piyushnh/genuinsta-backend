from celery.decorators import task
from celery.utils.log import get_task_logger
from fcm_django.models import FCMDevice
from .feed import notifManager


# import time
# from .feed import followFeedManager, TimelineFeed, FollowersFeed 


logger = get_task_logger(__name__)


@task(name="notify_task")
def notify_task(notif):
    """To be executed when a user follows someone"""
    try:
        if notif.type.lower() == 'notification':
            devices = FCMDevice.objects.filter(user=notif.recipient)
            devices.send_message(title="Title", body="Message",  data={"test": "test"})

        notifManager.add_notif(notif)

        return True

    except Exception as e:
        print(e)
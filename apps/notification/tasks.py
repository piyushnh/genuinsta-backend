from celery.decorators import task
from celery.utils.log import get_task_logger
from fcm_django.models import FCMDevice
from .feed import notifManager
from .models import Notification

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# import time
# from .feed import followFeedManager, TimelineFeed, FollowersFeed 


logger = get_task_logger(__name__)


# @task(name="notify_task")
# def notify_task(notif):
#     try:
#         if notif.type.lower() == 'notification':
#             devices = FCMDevice.objects.filter(user=notif.recipient)
#             devices.send_message(title="Title", body="Message",  data={"test": "test"})

#         notifManager.add_notif(notif)

#         return True

#     except Exception as e:
#         print(e)

@task(name="create_notif")
def create_notif(category, type, from_user_id, recipient_id, item_id):
    try:

        from_user = User.objects.get(user_id=from_user_id)
        to_user = User.objects.get(user_id=recipient_id)
        print('item -id')
        print(item_id)
        notif = Notification.objects.create(category=category, type=type, user=from_user, recipient=to_user, item_id=item_id)
        
        if type == 'NOTIFICATION':
            devices = FCMDevice.objects.filter(user=notif.recipient)
            devices.send_message(title="Title", body="Message",  data={"test": "test"})

        notifManager.add_notif(notif)
        

        return True

    except Exception as e:
        print(e)

@task(name="delete_fcm_token")
def delete_fcm_token(user_id, fcm_token):
    try:
        
        user = User.objects.get(user_id=user_id)
        device = FCMDevice.objects.get(user=user, registration_id=fcm_token, 
                                    type='web')
        device.delete()
        

        return True

    except Exception as e:
        print(e)

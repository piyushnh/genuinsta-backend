from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from rest_framework.decorators import api_view, permission_classes
from fcm_django.models import FCMDevice
from .feed import MyNotificationFeed
from .serializers import AggregatedActivitySerializer 
from celery.utils.log import get_task_logger

import logging
logger = logging.getLogger(__name__)





try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def notify(request):
    """
    """
    try:
       

        device = FCMDevice.objects.get(user=request.user)

        # device.send_message("Title", "Message")
        # device.send_message(data={"test": "test"})
        device.send_message(title="Title", body="Message",  data={"test": "test"})
            
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def set_fcm_token(request):
    """
    """
    try:
       
        data = request.data
        device, created = FCMDevice.objects.get_or_create(registration_id=data['registration_token'], 
                                    type='web')
        if not created :
            if not (device.user.user_id == request.user.user_id):
                device.delete()
                new_device = FCMDevice.objects.create(user=request.user, registration_id=data['registration_token'], 
                                    type='web')
            else:
                pass
        else:
            device.user = request.user
            device.save()

            
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_notifications(request):
    # """
    # """
    try:
        data = MyNotificationFeed(request.user.user_id)[:]
        print(data)

        if len(data) > 1:
            serializer = AggregatedActivitySerializer(data,  context={'request': request}, many = True)
            responseData = serializer.data
        elif len(data) == 1:
            serializer = AggregatedActivitySerializer(data[0],  context={'request': request})
            responseData = [serializer.data]
        else:
            return Response([], status=status.HTTP_200_OK)

        return Response(responseData , status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def mark_as_read(request):
    # """
    # """
    try:
        data = request.data
        activity_id = data['activityId']
        feed = MyNotificationFeed(request.user.user_id)

        feed.mark_activity(activity_id, read=True)


        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def sendify(request):
    # """
    # """
    try:
        from django_eventstream import send_event

        send_event('test', 'message', {'text': 'hello world'})


        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

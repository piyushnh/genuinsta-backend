from rest_framework import serializers

from .models import (PaytmHistory)

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User



class PaytmHistorySerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations


    class Meta:
        model = PaytmHistory
        fields = ['RESPMSG','RESPCODE', 'TXNID',  'STATUS']

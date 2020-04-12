from rest_framework import serializers


try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations


    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'is_merchant', 'mobile_number' ]
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
        fields = ['username','first_name', 'last_name', 'email',  'mobile_number' ]

class UserProfileSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',  'mobile_number', 'bio', 
                    'profile_picture', 'date_joined', 'id' ]




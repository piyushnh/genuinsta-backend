from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
# from django.contrib.auth.decorators import login_required
# from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    GenericAPIView,
    # CreateAPIView,
    # DestroyAPIView,
    # UpdateAPIView
)

from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
import requests
import json
from django.conf import settings

#Models and serializer imports
from apps.restaurants.models import Restaurant
from apps.restaurants.serializers import (OrderSerializer, RestaurantSerializer)



# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin





@api_view(['POST'])
@permission_classes([])
def merchant_login(request):
    
    try:
        email = request.data['email']
        password = request.data['password']

        try:
            user = User.objects.get(email = email)
            if user.is_merchant:
                res = requests.post("{}/rest-auth/login/".format(settings.ROOT_HOST_URL), data={'email': email, 'password':password})
                return Response(res, status = status.HTTP_200_OK)
            else:
                res_dict = {
                    'errorMessage': 'Must be a Restaurant Merchant to Login'
                }
                res_json = json.dumps(res_dict)
                return Response(res_json, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


    except:
        res_dict = {
                    'errorMessage': 'Oops! Something went wrong! Please try again.'
                }
        res_json = json.dumps(res_dict)
        return Response(res_json,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProcessingOrdersList(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(id=restaurant_id)
        orders = restaurant.orders.filter(Q(is_delivered = False),Q(is_paid = True))
    
        # items = categories.first().items

        return orders

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def get_restaurant(request, owner_id):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        restaurant = User.objects.get(id = owner_id).restaurants.all()
        print(restaurant[0])

        serialized_order = RestaurantSerializer(restaurant[0])
        
        return Response(serialized_order.data,status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


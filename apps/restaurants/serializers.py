from rest_framework import serializers

from .models import (Restaurant,
                    FoodCourt,
                    Menu,
                    MenuItem,
                    MenuCategory,
                    Order,
                    Quantity)

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User



class RestaurantSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer(read_only=True,many=True,) #method to include foreign relations


    class Meta:
        model = Restaurant
        fields = '__all__'

class FoodCourtSerializer(serializers.ModelSerializer):
    restaurants = RestaurantSerializer(read_only=True,many=True,) #method to include foreign relations

    class Meta:
        model = FoodCourt
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = '__all__'

class LightMenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = ['name','price']

class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(read_only=True,many=True,) #method to include foreign relations

    class Meta:
        model = MenuCategory
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    categories = MenuCategorySerializer(read_only=True,many=True,) #method to include foreign relations

    class Meta:
        model = Menu
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

class QuantitySerializer(serializers.ModelSerializer):
  class Meta:
    model = Quantity
    fields = ['id','number']

class RelatedRestaurantSerializer(serializers.ModelSerializer):
  class Meta:
    model = Restaurant
    fields = ['id', 'owner']


class OrderSerializer(serializers.ModelSerializer):
  quantities = QuantitySerializer(read_only=True,many=True,) #method to include foreign relations
  items = LightMenuItemSerializer(read_only=True,many=True,) #method to include foreign relations
#   customer = UserSerializer(read_only=True,) #method to include foreign relations
  restaurant = RelatedRestaurantSerializer(read_only=True,) #method to include foreign relations

  class Meta:
    model = Order
    fields = '__all__'


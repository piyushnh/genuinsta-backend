from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from . import views

from .views import (NearbyRestaurantsView,
                    NearbyFoodCourtsView,
                    FoodCourtRestaurantList,
                    MenuItemList,
                    create_order,
                    OrderSummary,
                    MenuItemDetail,
                    RestaurantDetail,
                    ResetOrder
                    )

urlpatterns = [
    url(r'^nearby/',view = NearbyRestaurantsView.as_view(),name="nearbyrestaurants" ),
    url(r'^nearbyfoodcourts/',view = NearbyFoodCourtsView.as_view() ,name="nearbyfoodcourts"),
    url(r'^foodcourt/members/(?P<foodcourt_id>[\w-]+)/$',
            view = cache_page(CACHE_TTL)(FoodCourtRestaurantList.as_view()),
             name="food_court_restaurants" ),

    url(r'^menuitems/(?P<restaurant_id>[\w-]+)/$',
            view = cache_page(CACHE_TTL)(MenuItemList.as_view()),
             name="menu_item_list" ),
    url(r'^get_menuitem/(?P<menuitem_id>[\w-]+)/$',
            view = cache_page(CACHE_TTL)(MenuItemDetail.as_view()),
             name="menu_item_detail" ),
    url(r'^restaurant/(?P<restaurant_id>[\w-]+)/$',
            view = cache_page(CACHE_TTL)(RestaurantDetail.as_view()),
             name="restaurant_detail" ),
    url(r'^reset_order/(?P<order_id>[\w-]+)/$',
            view = ResetOrder.as_view(),
             name="reset_order" ),

    url(r'^order/create/$',
            view =create_order,
             name="create_order" ),

    url(r'^order_details/(?P<pk>[\w-]+)/$',
            view =OrderSummary.as_view(),
             name="order_summary" ),
             


]

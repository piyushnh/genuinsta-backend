from django.contrib import admin
from django.urls import path
from django.urls import path
from django.conf import settings
from . import views

from .views import (merchant_login,
                    ProcessingOrdersList,
                    get_restaurant
                    )

urlpatterns = [
    

    path('login/',
            merchant_login ),
    path('processing_orders/<str:restaurant_id>',
            ProcessingOrdersList.as_view()),
    path('restaurant_owned/<str:owner_id>',
            get_restaurant)

]

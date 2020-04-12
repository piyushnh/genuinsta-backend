from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings

from .views import initiatePayment, response, order_response

urlpatterns = [
    url(r'^initiate_payment/$',view = initiatePayment,name="paytm_payment" ),
    url(r'^response/$',view = response,name="paytm_response" ),
    url(r'^order_response/(?P<order_id>[\w-]+)/$',view = order_response,name="paytm_order_response" ),



]

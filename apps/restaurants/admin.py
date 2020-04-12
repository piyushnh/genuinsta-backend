from django.contrib import admin
from django.contrib.gis.db import models
from django.contrib.gis.admin import OSMGeoAdmin
from .models import (Restaurant,
                     FoodCourt,
                     Menu,
                     MenuCategory,
                     MenuItem,
                     Order,
                     Quantity,
                     )
# from .models import Restaurant
# # Register your models here.
#
admin.site.register(Menu)
admin.site.register(Quantity)
admin.site.register(Order)
admin.site.register(MenuCategory)
admin.site.register(MenuItem)



@admin.register(Restaurant)
class RestaurantAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')

@admin.register(FoodCourt)
class FoodCourtAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')

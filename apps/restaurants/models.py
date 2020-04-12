from django.contrib.gis.db import models as gis_models
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid

from django.contrib.gis import geos
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError

from apps.paytm.models import MerchantProfile as PaytmMerchantProfile

from django.core.validators import MaxValueValidator, MinValueValidator

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
# Create your models here.



class FoodCourt(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length=100, null=True)
    cover_pic = models.ImageField(upload_to = 'media/foodcourt_pics',blank=False )
    location = gis_models.PointField(u"longitude/latitude",
                                     geography=True, blank=True, null=True)
    phone_number = models.CharField(max_length = 10, blank=False)
    website_url = models.URLField(max_length=100, default='')
    city = models.CharField(max_length=50, default="Banglore")

    gis = gis_models.Manager()
    objects = models.Manager()
    # gis = gis_models.GeoManager()


    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #            return reverse("restaurants:restaurant_detail", kwargs = {'pk':self.pk})
    def save(self, **kwargs):
        if not self.location:
            address = u'%s %s' % (self.city, self.address)
            address = address.encode('utf-8')
            geocoder = GoogleV3(api_key = 'AIzaSyA0bGrFzBs4jnhV5Lxb0Rfc-YIeJ4Lv2gw')
            try:
                _, latlon = geocoder.geocode(address)
                print(latlon)
            except (GeocoderQueryError, ValueError):
                pass
            else:
                point = "POINT(%s %s)" % (latlon[1], latlon[0])
                self.location = geos.fromstr(point)
        super(FoodCourt, self).save()

class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants', null=True, blank=True)
    foodcourt = models.ForeignKey(FoodCourt, on_delete=models.CASCADE, related_name='restaurants', null=True, blank=True)
    address = models.CharField(max_length=100, null=True)
    cover_pic = models.ImageField(upload_to = 'media/restaurant_pics',blank=False )
    location = gis_models.PointField(u"longitude/latitude",
                                     geography=True, blank=True, null=True)
    phone_number = models.CharField(max_length = 10, blank=False)
    website_url = models.URLField(max_length=100, default='')
    city = models.CharField(max_length=50, default="Banglore")

    gis = gis_models.Manager()
    objects = models.Manager()


    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #            return reverse("restaurants:restaurant_detail", kwargs = {'pk':self.pk})

    def save(self, **kwargs):
        if not self.location:
            address = u'%s %s' % (self.city, self.address)
            address = address.encode('utf-8')
            geocoder = GoogleV3(api_key = 'AIzaSyA0bGrFzBs4jnhV5Lxb0Rfc-YIeJ4Lv2gw')
            try:
                _, latlon = geocoder.geocode(address)
                print(latlon)
            except (GeocoderQueryError, ValueError):
                pass
            else:
                point = "POINT(%s %s)" % (latlon[1], latlon[0])
                self.location = geos.fromstr(point)
        super(Restaurant, self).save()

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='review')
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    review = models.CharField(max_length=10000, blank=False)

    def __str__(self):
        return str(self.restaurant)

class Ratings(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return str(self.restaurant)

class Menu(models.Model):
   name = models.CharField(max_length=24, unique=True, verbose_name='menu name')
   slug = models.SlugField(max_length=24, unique=True, help_text='The slug is the URL friendly version of the menu name, so that this can be accessed at a URL like mysite.com/menus/dinner/.')
   restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu', null=True,blank=True)
   additional_text = models.CharField(max_length=128, null=True, blank=True, help_text='Any additional text that the menu might need, i.e. Served between 11:00am and 4:00pm.')
   order = models.PositiveSmallIntegerField(default=0, help_text='The order of the menu determines where this menu appears alongside other menus.')

   class Meta:
      verbose_name='menu'
      verbose_name_plural='menu'

   def __str__(self):
     return str(self.restaurant)

"""
A Menu Category represents a grouping of items within a specific Menu.
An example of a Menu Category would be Appetizers, or Pasta.
"""
class MenuCategory(models.Model):
	menu = models.ForeignKey(Menu,on_delete=models.CASCADE,related_name='categories', help_text='The menus that this category belongs to, i.e. \'Lunch\'.')
	name = models.CharField(max_length=32, verbose_name='menu category name')
	additional_text = models.CharField(max_length=128, null=True, blank=True, help_text='The additional text is any bit of related information to go along with a menu category, i.e. the \'Pasta\' category might have details that say \'All entrees come with salad and bread\'.')
	order = models.IntegerField(default=0, help_text='The order is the order that this category should appear in when rendered on the templates.')

	class Meta:
		verbose_name='menu category'
		verbose_name_plural='menu categories'
		ordering = ['order', 'name']

	def __str__(self):
		return str(self.menu)+"-"+str(self.name)

"""
A Menu Item is an item of food that the restaurant makes. A Menu Item can
belong to multiple Menu Categories to facilitate menus that have the same item
across multiple menus.
"""
class MenuItem(models.Model):
    CLASSIFICATION_CHOICES = (
    	('non-vegetarian', 'Non-Vegetarian'),
    	('vegan', 'Vegan'),
    	('vegetarian', 'Vegetarian'),
    )

    name = models.CharField(max_length=48, help_text='Name of the item on the menu.')
    description = models.CharField(max_length=128, null=True, blank=True, help_text='The description is a simple text description of the menu item.')
    category = models.ManyToManyField(MenuCategory,related_name='items', verbose_name='menu category', help_text='Category is the menu category that this menu item belongs to, i.e. \'Appetizers\'.')
    order = models.IntegerField(default=0, verbose_name='order', help_text='The order is to specify the order in which items show up on the menu.')
    price = models.IntegerField(help_text='The price is the cost of the item.')
    image = models.ImageField(upload_to='media/menu_item_pics', null=True, blank=True, verbose_name='image', help_text='The image is an optional field that is associated with each menu item.')

    classification = models.CharField(max_length=20, choices=CLASSIFICATION_CHOICES, default=0, verbose_name='classification', help_text='Select if this item classifies as Vegetarian, Vegan, or Neither.')
    spicy = models.BooleanField(default=False, verbose_name='spicy?', help_text='Is this item spicy?')
    contains_peanuts = models.BooleanField(default=True, verbose_name='contain peanuts?', help_text='Does this item contain peanuts?')
    gluten_free = models.BooleanField(default=False, verbose_name='gluten free?', help_text='Is this item Gluten Free?')
    popular = models.BooleanField(default=False, verbose_name='Popular?', help_text='Is this item popular?')

    class Meta:
    	verbose_name='menu item'
    	verbose_name_plural='menu items'
    	# ordering = ['order', 'name','scategory']

    def __unicode__(self):
    	return self.name

    def __str__(self):
       return str(self.name)


class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length = 15)
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders',  )
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name='orders',)
    amount = models.IntegerField(default=0, verbose_name='amount', )
    items = models.ManyToManyField(MenuItem, related_name='orders')#name orders means all the orders a dish has been a part of
    is_paid = models.BooleanField(default=False)    
    is_placed = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return str(self.order_id)

    def save(self, *args, **kwargs):
        while not self.order_id:
            newId = str(uuid.uuid4()).replace('-','')[0:10]

            if not Order.objects.filter(order_id = newId).exists():
                self.order_id = newId

        super().save(*args, **kwargs)

class Quantity(models.Model):
    number = models.IntegerField(default=0)
    order = models.ForeignKey(Order,on_delete=models.CASCADE, related_name='quantities',null=True )

    def __str__(self):
        return str(self.number)

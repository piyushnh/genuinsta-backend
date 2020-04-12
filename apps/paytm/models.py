from django.db import models

from django.utils import timezone

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
# Create your models here.

class MerchantProfile(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name='paytm_merchant', help_text='The User this restaurant belongs to')
    # phone_number = models.CharField(max_length = 10, blank=False)
    merchant_id = models.CharField(max_length=20, unique=True, primary_key=True)
    key = models.CharField(max_length=20, unique=True)



    def __str__(self):
        return str(self.owner)

class PaytmHistory(models.Model):
    customer = models.ForeignKey(User,on_delete = models.CASCADE ,related_name='paytm_payments',null=True)
    ORDERID = models.CharField('ORDER ID', max_length=50)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    TXNID = models.CharField('TXN ID', max_length=64)
    BANKTXNID = models.CharField('BANK TXN ID',max_length=50, null=True, blank=True)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.CharField('RESP CODE', max_length=10)
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=15, null=True, blank=True)
    MID = models.CharField(max_length=20)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.CharField('TXN AMOUNT', max_length=10)
    STATUS = models.CharField('STATUS', max_length=20)
    CUST_ID = models.CharField('CUST_ID', max_length=64)


    class Meta:
        app_label = 'paytm'

    def __unicode__(self):
        return self.STATUS

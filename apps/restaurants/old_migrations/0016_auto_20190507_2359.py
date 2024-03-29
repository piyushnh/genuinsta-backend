# Generated by Django 2.1.7 on 2019-05-07 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0015_order_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10)),
                ('paytm_merchant_id', models.CharField(max_length=20, unique=True)),
                ('paytm_merchant_key', models.CharField(max_length=20, unique=True)),
                ('merchant', models.OneToOneField(help_text="The menus that this category belongs to, i.e. 'Lunch'.", on_delete=django.db.models.deletion.CASCADE, related_name='merchant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='merchant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to='restaurants.MerchantProfile'),
        ),
    ]

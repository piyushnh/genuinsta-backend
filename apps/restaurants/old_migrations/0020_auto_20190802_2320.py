# Generated by Django 2.1.7 on 2019-08-02 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0019_auto_20190802_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='paytm_merchant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to='paytm.MerchantProfile'),
        ),
    ]

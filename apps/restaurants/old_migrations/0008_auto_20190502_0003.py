# Generated by Django 2.1.7 on 2019-05-01 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0007_auto_20190501_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='foodcourt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='restaurants.FoodCourt'),
        ),
    ]

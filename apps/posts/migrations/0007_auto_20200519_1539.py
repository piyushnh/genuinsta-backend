# Generated by Django 2.1.7 on 2020-05-19 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20200519_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='hashtag',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
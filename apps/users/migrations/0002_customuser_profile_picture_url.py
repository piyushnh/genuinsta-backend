# Generated by Django 2.1.7 on 2020-07-22 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture_url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
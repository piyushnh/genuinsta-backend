# Generated by Django 2.2.15 on 2020-08-07 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='category',
            field=models.CharField(choices=[('FRIEND_REQUEST_SENT', 'friend_request'), ('FOLLOWING', 'following'), ('FRIEND_REQUEST_ACCEPTED', 'friend_request_accepted'), ('COMMENTED', 'commented')], max_length=20),
        ),
    ]
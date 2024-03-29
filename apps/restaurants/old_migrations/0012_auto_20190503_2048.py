# Generated by Django 2.1.7 on 2019-05-03 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0011_auto_20190503_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='classification',
            field=models.CharField(choices=[('non-vegetarian', 'Non-Vegetarian'), ('vegan', 'Vegan'), ('vegetarian', 'Vegetarian')], default=0, help_text='Select if this item classifies as Vegetarian, Vegan, or Neither.', max_length=20, verbose_name='classification'),
        ),
    ]

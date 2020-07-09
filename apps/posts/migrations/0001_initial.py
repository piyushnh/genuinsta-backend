# Generated by Django 2.1.7 on 2020-07-08 19:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smartfields.fields
import smartfields.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('bookmark_id', models.IntegerField(primary_key=True, serialize=False)),
                ('bookmark_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('comment_time', models.DateTimeField(auto_now_add=True)),
                ('comment_type', models.CharField(choices=[('TEXT', 'text'), ('IMAGE', 'image'), ('STICKER', 'sticker')], default='TEXT', max_length=7)),
                ('text', models.TextField(null=True)),
                ('commentSrc', models.ImageField(upload_to='comment_images_stickers')),
                ('comment_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('hashtag_id', models.IntegerField(primary_key=True, serialize=False)),
                ('hashtag_time', models.DateTimeField(auto_now_add=True)),
                ('hashtag', models.CharField(max_length=1000, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('like_id', models.IntegerField(primary_key=True, serialize=False)),
                ('like_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('image', smartfields.fields.ImageField(upload_to='post')),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('location', models.TextField(null=True)),
                ('privacy_type', models.CharField(choices=[('FRIENDS', 'friends'), ('FOLLOWERS', 'followers')], default='FRIENDS', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(smartfields.models.SmartfieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PostTags',
            fields=[
                ('post_tag_id', models.IntegerField(primary_key=True, serialize=False)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_tags', to='posts.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_tags', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileViews',
            fields=[
                ('view_id', models.IntegerField(primary_key=True, serialize=False)),
                ('view_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('view_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_views', to=settings.AUTH_USER_MODEL)),
                ('view_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_views', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('recommend_id', models.IntegerField(primary_key=True, serialize=False)),
                ('recommend_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('recommend_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_recommendatiions', to=settings.AUTH_USER_MODEL)),
                ('recommend_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommends', to='posts.Post')),
                ('recommend_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_recommendatiions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_id', models.IntegerField(primary_key=True, serialize=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='posts.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='posts',
            field=models.ManyToManyField(related_name='hashtags', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]

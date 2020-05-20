from django.db.models.signals import post_save
from django.dispatch import receiver
import re
from .models import Post, HashTag

@receiver(post_save, sender=Post)
def add_hashtags(sender, instance, **kwargs):
    try: 
        post_desc =  instance.desc
        hashtags = re.findall(r"#(\w+)". post_desc)

        for h in hashtags:
            h = h.lower()
            hashtag = Hashtags.objects.get_or_create(hashtag = h)
            hashtag.posts.add(instance)
    except Exception as e:
        print(e)


        


    



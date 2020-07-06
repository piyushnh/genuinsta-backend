from celery.decorators import task
from celery.utils.log import get_task_logger
from stream_django.feed_manager import feed_manager
import time



logger = get_task_logger(__name__)


@task(name="after_following_task")
def after_following_task(follower_id, followee_id):
    """To be executed when a user follows someone"""
    try:
        # time.wait(20)

        followee_feed = feed_manager.get_feed('followers', followee_id)
        follower_timeline = feed_manager.get_feed('timeline', follower_id)

        follower_timeline.follow(followee_feed.slug, followee_feed.user_id)  
        logger.info("Done")

        return 'hellos'

    except Exception as e:
        print(e)

@task(name="after_unfollowing_task")
def after_unfollowing_task(follower_id, followee_id):
    """To be executed when a user unfollows someone"""
    try:
        # time.wait(20)

        followee_feed = feed_manager.get_feed('followers', followee_id)
        follower_timeline = feed_manager.get_feed('timeline', follower_id)

        follower_timeline.unfollow(followee_feed.slug, followee_feed.user_id, keep_history=True)  
        logger.info("Done")

        return 'hellos'

    except Exception as e:
        print(e)

@task(name="after_friending_task")
def after_friending_task(from_user_id, to_user_id):
    """To be executed when a user friends someone"""
    try:
        # time.wait(20)

        followee_feed = feed_manager.get_feed('followers', to_user_id)
        friends_feed = feed_manager.get_feed('friends', to_user_id)

        follower_timeline = feed_manager.get_feed('timeline', from_user_id)

        follower_timeline.follow(followee_feed.slug, followee_feed.user_id) 
        follower_timeline.follow(friends_feed.slug, friends_feed.user_id) 


        logger.info("Done")

        return 'hellos'

    except Exception as e:
        print(e)

@task(name="after_unfriending_task")
def after_unfriending_task(from_user_id, to_user_id):
    """To be executed when a user unfriends someone"""
    try:
        # time.wait(20)

        followee_feed = feed_manager.get_feed('followers', to_user_id)
        friends_feed = feed_manager.get_feed('friends', to_user_id)

        follower_timeline = feed_manager.get_feed('timeline', from_user_id)

        follower_timeline.unfollow(followee_feed.slug, followee_feed.user_id) 
        follower_timeline.unfollow(friends_feed.slug, friends_feed.user_id) 


        logger.info("Done")

        return 'hellos'

    except Exception as e:
        print(e)
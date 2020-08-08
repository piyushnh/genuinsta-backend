from celery.decorators import task
from celery.utils.log import get_task_logger
from apps.friendship.models import followFeedManager, friendFeedManager


# from feedback.emails import send_feedback_email

logger = get_task_logger(__name__)


@task(name="after_posting_task")
def after_posting_task(post):
    try:
        if post.privacy_type.lower() == 'friends':
                friendFeedManager.add_post(post)
        elif post.privacy_type.lower() == 'followers':
                followFeedManager.add_post(post)
                friendFeedManager.add_post(post)

        return 'hellos'

    except Exception as e:
        print(e)

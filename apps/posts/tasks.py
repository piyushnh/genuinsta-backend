from celery.decorators import task
from celery.utils.log import get_task_logger

# from feedback.emails import send_feedback_email

logger = get_task_logger(__name__)

from .models import Post, HashTag

# @task(name="create_hashtags")
# def send_feedback_email_task(post, description):
#     """sends an email when feedback form is filled successfully"""
#     logger.info("Sent feedback email")
#     return send_feedback_email(email, message)

import shlex
import subprocess

from django.core.management.base import BaseCommand
# from django.utils import autoreload
from django.conf import settings
import os


def restart_celery(*args, **kwargs):
    kill_worker_cmd = 'pkill -9 celery'
    subprocess.call(shlex.split(kill_worker_cmd))
    start_worker_cmd = 'celery -A influence worker -l info'
    subprocess.call(shlex.split(start_worker_cmd))


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Starting celery worker with autoreload...')



        # if settings.DEBUG:


        #     # print(os.environ.get('WERKZEUG_RUN_MAIN'))

        #     if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN') :
        #         import ptvsd


        #         ptvsd.enable_attach(address=('localhost', 7913))
        #         print('Debugger Attached!')

        try:
                from django.utils.autoreload import run_with_reloader
                run_with_reloader(restart_celery, args=None, kwargs=None)
        except ImportError:
                from django.utils import autoreload
                autoreload.main(restart_celery, args=None, kwargs=None)
        # autoreload.main(restart_celery, args=None, kwargs=None)
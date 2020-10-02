#!/usr/bin/env python
import os
import sys

# import multiprocessing
# multiprocessing.set_start_method('spawn', True)

if __name__ == '__main__':
    os.environ.setdefault('C_FORCE_ROOT', 'true')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'influence.settings')

    from django.conf import settings


    if settings.DEBUG:
        # import socket
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.close()



        if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN') :
            import ptvsd

            try:
                ptvsd.enable_attach(address=('localhost', 7913))
                print('Debugger Attached!')
            except OSError:
                print("ptvsd port already in use.")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

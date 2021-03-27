import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    subprocess.call(shlex.split('pkill -f "celery worker"'))
    subprocess.call(shlex.split(
        'celery worker -A django_celery_example --loglevel=info -Q high_priority,default'
    ))


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Starting celery worker with autoreload...')
        autoreload.run_with_reloader(restart_celery)

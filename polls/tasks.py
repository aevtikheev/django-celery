import random

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from celery.signals import task_postrun
from django.core.management import call_command

from polls.consumers import notify_channel_layer


logger = get_task_logger(__name__)


@shared_task()
def sample_task(email):
    from polls.views import api_call

    api_call(email)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={'max_retries': 5},
)
def task_process_notification(self):
    if not random.choice([0, 1]):
        raise Exception()

    requests.post('https://httpbin.org/delay/5')


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    """
    When celery task finish, send notification to Django channel_layer,
    so Django channel would receive the event and then send it to web client.
    """
    notify_channel_layer(task_id)


@shared_task(name='task_clear_session')
def task_clear_session():
    call_command('clearsessions')


@shared_task(name='default:dynamic_example_one')
def dynamic_example_one():
    logger.info('Example One')


@shared_task(name='low_priority:dynamic_example_two')
def dynamic_example_two():
    logger.info('Example Two')


@shared_task(name='high_priority:dynamic_example_three')
def dynamic_example_three():
    logger.info('Example Three')

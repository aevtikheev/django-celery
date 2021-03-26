import logging
import random

import requests
from celery.result import AsyncResult
from celery.states import FAILURE
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from polls.forms import YourForm
from polls.tasks import sample_task, task_process_notification

logger = logging.getLogger(__name__)


def api_call(email):
    if random.choice([0, 1]):
        raise Exception('random processing error')

    requests.post('https://httpbin.org/delay/5')


def form(request):
    if request.is_ajax() and request.method == 'POST':
        submit_task_form = YourForm(request.POST)
        if submit_task_form.is_valid():
            task = sample_task.delay(submit_task_form.cleaned_data['email'])
            return JsonResponse({
                'task_id': task.task_id,
            })

    submit_task_form = YourForm()
    return render(request, 'form.html', {'form': submit_task_form})


def task_status(request):
    task_id = request.GET.get('task_id')

    if task_id:
        task = AsyncResult(task_id)
        if task.state == FAILURE:
            response = {
                'state': task.state,
                'error': str(task.result),
            }
        else:
            response = {
                'state': task.state,
            }
        return JsonResponse(response)


@csrf_exempt
def webhook_test(request):
    if not random.choice([0, 1]):
        # mimic an error
        raise Exception()

    # blocking process
    requests.post('https://httpbin.org/delay/5')
    return HttpResponse('pong')


@csrf_exempt
def webhook_test2(request):
    task = task_process_notification.delay()
    logger.info(task.id)
    return HttpResponse('pong')

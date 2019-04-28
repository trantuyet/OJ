import json
from functools import partial
from urllib.parse import urlencode
from uuid import UUID

from celery.result import AsyncResult
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import is_safe_url

from judge.tasks import success, failure, progress
from judge.utils.views import short_circuit_middleware


def get_task_status(task_id):
    result = AsyncResult(task_id)
    if result.state == 'PROGRESS':
        return {'code': 'PROGRESS', 'done': result.result['done'], 'total': result.result['total']}
    elif result.state == 'SUCCESS':
        return {'code': 'SUCCESS'}
    elif result.state == 'FAILURE':
        return {'code': 'FAILURE', 'error': str(result.result)}
    else:
        return {'code': 'WORKING'}


def task_status(request, task_id):
    try:
        UUID(task_id)
    except ValueError:
        raise Http404()

    redirect = request.GET.get('redirect')
    if not is_safe_url(redirect, allowed_hosts={request.get_host()}):
        redirect = None

    status = get_task_status(task_id)
    if status['code'] == 'SUCCESS' and redirect:
        return HttpResponseRedirect(redirect)

    return render(request, 'task_status.html', {
        'task_id': task_id, 'task_status': json.dumps(status),
        'message': request.GET.get('message', ''), 'redirect': redirect or ''
    })


@short_circuit_middleware
def task_status_ajax(request):
    if 'id' not in request.GET:
        return HttpResponseBadRequest('Need to pass GET parameter "id"', content_type='text/plain')
    return JsonResponse(get_task_status(request.GET['id']))


def demo_task(request, task, message):
    if not request.user.is_superuser:
        raise PermissionDenied()
    result = task.delay()
    return HttpResponseRedirect(reverse('task_status', args=[result.id]) + '?' + urlencode({
        'message': message, 'redirect': reverse('home')
    }))


demo_success = partial(demo_task, task=success, message='Running example task that succeeds...')
demo_failure = partial(demo_task, task=failure, message='Running example task that fails...')
demo_progress = partial(demo_task, task=progress, message='Running example task that waits 10 seconds...')

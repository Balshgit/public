from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .tasks import process_download
from django.views.decorators.http import require_http_methods
from celery.result import AsyncResult


task_id = {}


def demo_view(request: HttpRequest) -> HttpResponse:
    username = str(request.user.username)
    if request.method == 'POST':
        # Create Task
        download_task = process_download.delay()
        # Get ID
        task_id[username] = download_task.task_id
        # Print Task ID
        print(f'Celery Task ID: {task_id[username]}')
        # Return demo view with Task ID
        return render(request, 'progress.html', {'task_id': task_id[username]})
    else:
        # Return demo view
        return render(request, 'progress.html', {})

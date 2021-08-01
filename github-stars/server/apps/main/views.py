from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import GithubForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .commands import get_github_stars, process_download
from django.views.decorators.http import require_http_methods
from celery.result import AsyncResult


task_id = {}


def index(request: HttpRequest) -> HttpResponse:
    """
    Main (or index) view.

    Returns rendered default page to the user.
    Typed with the help of ``django-stubs`` project.
    """
    return render(request, 'main/index.html')


@login_required
def github(request: HttpRequest) -> HttpResponse:
    username = str(request.user.username)
    try:
        email = getattr((User.objects.get(username=username)),
                        'email', 'default@email.ru')

    except ObjectDoesNotExist as e:
        error = 'That user doesnt exists or not log on'
        print(error, e)

    if request.method == 'POST':

        github_username = str(request.POST.get('search_field'))
        result = get_github_stars.delay(github_username)
        task_id[username] = result.task_id

        return redirect(reverse('github_result'))

    form = GithubForm
    return render(request, 'main/github.html',
                  context={'form': form})


@login_required
@require_http_methods(['GET'])
def github_result(request: HttpRequest) -> HttpResponse:
    username = str(request.user.username)
    data = AsyncResult(task_id[username])

    if data.ready():
        message = "Result Ready"
        result = data.get()
        print('result ready')
    else:
        print('result not ready')

    return render(request, 'main/github_result.html',
                  context={'data': result,
                           'message': message})


def demo_view(request: HttpRequest) -> HttpResponse:
    username = str(request.user.username)
    form = GithubForm
    result = {}
    message = ''

    if request.method == 'GET':
        try:
            data = AsyncResult(task_id[username])
            if data.ready():
                result = data.get()
                message = f'Total repos: {len(result)}\n'
                if len(result) == 0:
                    result = {'Error': 'User has no repositories!'}
                print('Result ready! Please refresh page')
            else:
                print('result not ready')
        except KeyError as e:
            print(e)
        finally:
            # Return demo view
            return render(request, 'progress.html',
                          context={'data': result, 'form': form,
                                   'message': message})

    elif request.method == 'POST':
        message = 'Please wait'
        github_username = str(request.POST.get('search_field'))
        # Create Task
        result = get_github_stars.delay(username=github_username)

        # Get ID
        task_id[username] = result.task_id
        # Print Task ID
        print(f'Celery Task ID: {task_id[username]}')
        # Return demo view with Task ID
        return render(request, 'progress.html',
                      context={'task_id': task_id[username],
                               'message': message,
                               'data': {}})

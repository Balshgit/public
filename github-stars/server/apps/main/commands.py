import requests
from requests.models import Response
from requests.auth import HTTPBasicAuth
import re
import time
from functools import lru_cache
from typing import Dict, Optional
from server.apps.main.celery_config import celery_app
from server.settings.components.common import GIT_API_URL
from celery_progress.backend import ProgressRecorder
from celery import shared_task
from server.settings.components import config


def current_page(response: Response, link: str) -> int:
    url = str(response.links[f'{link}']['url'])
    page_count = int(str(re.findall(pattern=r'page=\d+', string=url)[1])
                     .replace('page=', ''))
    return page_count


def github_request(url: str) -> Response:
    auth = HTTPBasicAuth(config('GITHUB_USERNAME'), config('GITHUB_PASSWORD'))
    counter = 0
    while True:
        try:
            counter += 1
            if auth == HTTPBasicAuth('', ''):
                response = requests.get(url)
            else:
                response = requests.get(url, auth=auth)
            return response
        except ConnectionError as connection_error:
            if counter < 5:
                time.sleep(10)
            else:
                raise connection_error


@shared_task(bind=True)
def get_github_stars(self, username: str) -> Dict[str, Optional[int]]:

    url = f'{GIT_API_URL}/{username}/repos?per_page=100&page=1'
    print(url)
    progress_recorder = ProgressRecorder(self)

    response = github_request(url)
    if response.status_code >= 400:
        result = {}
    else:
        repos = response.json()

        try:
            page_count = current_page(response, 'last')
            repos_count = (page_count - 1) * 100 + \
                          len(github_request(response.links['last']['url']).json())
        except KeyError as e:
            page_count = 1
            repos_count = len(repos)

        i = 0
        while 'next' in response.links.keys():
            i += 1
            response = github_request(response.links['next']['url'])
            repos.extend(response.json())
            current = i * 100 + len(response.json())

            # Progress bar
            percent = round(100 / page_count * i)
            progress_recorder.set_progress(current, repos_count,
                                           description=f'Processing: {percent}%')

        # Fetching repos and stars in dict
        data: Dict[str, int] = {}
        try:
            for item in repos:
                data[item['name']] = int(item['stargazers_count'])
            result = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
        except TypeError:
            result = {}

    return result


@shared_task(bind=True)
def process_download(self):
    print('Task started')
    # Create the progress recorder instance
    # which we'll use to update the web page
    progress_recorder = ProgressRecorder(self)

    print('Start')
    for i in range(5):
        # Sleep for 1 second
        time.sleep(1)
        # Print progress in Celery task output
        print(i + 1)
        # Update progress on the web page
        progress_recorder.set_progress(i + 1, 5, description='Downloading')
    print('End')

    return 'Task Complete'

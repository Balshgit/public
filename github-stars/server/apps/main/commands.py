import re
import time
import sys
from typing import Dict, Optional, Tuple
from server.apps.main.celery_config import celery_app
from server.settings.components.common import GIT_API_URL
from celery_progress.backend import ProgressRecorder
from celery import shared_task
from server.settings.components import config
import aiohttp
import asyncio
import logging

console_logger = logging.getLogger(__name__)
formatter = logging.Formatter(datefmt="%Y.%m.%d %H:%M:%S",
                              fmt='%(asctime)s | message: %(message)s')
                              # fmt='%(asctime)s | %(levelname)s | process: %(process)d | module name: %(name)s | '
                              #     'func name: %(funcName)s | line number: %(lineno)s | message: %(message)s',)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
console_logger.setLevel(logging.INFO)
console_logger.addHandler(handler)


class GitHubScanner:
    def __init__(self, user: str, token: str):
        self.auth = aiohttp.BasicAuth(user, token)
        self.data = {}
        self.semaphore = asyncio.Semaphore(200)

    def _data_count(self) -> int:
        repos_count = 0
        try:
            for data_set in self.data.values():
                repos_count += len(data_set['data'])
        except ValueError:
            console_logger.info(f'Data is empty')
        return repos_count

    @staticmethod
    def _page_count(url: str) -> int:
        page = int(str(re.findall(pattern=r'&page=\d+', string=url)[-1]).replace('&page=', ''))
        return page

    async def _github_request(self, session: aiohttp.ClientSession, url: str) -> Dict:
        async with self.semaphore:
            counter = 0
            while True:
                try:
                    counter += 1
                    resp = await session.get(url)
                    async with resp:
                        if resp.status == 200:
                            self.data[self._page_count(url)] = {'response': resp, 'data': await resp.json()}
                            return self.data[self._page_count(url)]
                        if resp.status >= 400:
                            return {'response': None, 'data': None}
                except Exception as connection_error:
                    if counter < 5:
                        await asyncio.sleep(10)
                    else:
                        raise connection_error

    async def get_data(self, celery_task, username: str) -> None:
        base_url = f'{GIT_API_URL}/{username}/repos?per_page=100&page=' + '{}'
        progress_recorder = ProgressRecorder(celery_task)
        connector = aiohttp.TCPConnector(limit=500)
        async with aiohttp.ClientSession(auth=self.auth, connector=connector) as session:
            url = base_url.format(1)
            tasks = []
            try:
                resp = await self._github_request(session, url)
                self.data[1] = resp
                last_page = self._page_count(dict(resp['response'].headers).get('Link'))
                last_page_url = str(resp['response'].links['last']['url'])
                if last_page:
                    data_last_page = await self._github_request(session, last_page_url)
                    repos_count = (last_page - 1) * 100 + len(data_last_page['data'])
                    for i in range(1, last_page):
                        url = base_url.format(i + 1)
                        current_repos_count = self._data_count()
                        percent = round(current_repos_count / repos_count * 100)
                        progress_recorder.set_progress(current_repos_count, repos_count,
                                                       description=f'Processing: {percent}%')
                        task = asyncio.create_task(self._github_request(session, url))
                        tasks.append(task)
                else:
                    tasks.append(asyncio.create_task(self._github_request(session, url)))
            except Exception as e:
                console_logger.error(e)
            await asyncio.gather(*tasks)


@celery_app.task(bind=True)
def get_github_stars(celery_task, username: str) -> Dict[str, Optional[int]]:
    github = GitHubScanner(config('GITHUB_USERNAME'), config('GITHUB_TOKEN'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(github.get_data(celery_task, username))
    repos_data = github.data
    data = {}
    try:
        for value in repos_data.values():
            for item in value['data']:
                data[item["name"]] = item["stargazers_count"]
        result = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    except TypeError:
        result = {}
    return result


# Demo task
@shared_task(bind=True)
def process_download(task) -> str:
    print('Task started')
    # Create the progress recorder instance
    # which we'll use to update the web page
    progress_recorder = ProgressRecorder(task)

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

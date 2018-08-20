import asyncio
import logging
from contextlib import closing
import aiohttp # $ pip install aiohttp
import os
import posixpath
from urllib.parse import urlsplit, unquote
logger = logging.getLogger()
from bs4 import BeautifulSoup
import requests
from .filesystem import url_to_filename

async def get_web(url, parser = 'html.parser'):
    try:
        r = requests.get(url)
        return BeautifulSoup(r.content.decode('utf-8'), parser)
    except:
        return None



class DownloadItem:
    def __init__(self,original_url,target_path):
        self.original_url = original_url
        self.target_path = target_path

class ParallelDownloader:
    def __init__(self,urls,target_path,done_callback, **kwargs):
        self.urls = urls
        self.done_callback = done_callback
        self.downloaded_items = []
        self.target_path = target_path
        self.args = kwargs

    @asyncio.coroutine
    def download(self,url, session, semaphore, chunk_size=1 << 15):
        with (yield from semaphore):  # limit number of concurrent downloads
            try:
                filename = url_to_filename(url)
            except:
                filename = "error.png"
            filename = os.path.join(self.target_path, filename)
            logger.info('Downloading {} to {}'.format(url,filename))
            response = None
            try:
                response = yield from session.get(url)
            except Exception as ex:
                logger.error("Error trying to download URL {}".format(url))
                logger.error(ex)
            if response is not None:
                with closing(response), open(filename, 'wb') as file:
                    while True:  # save file
                        chunk = yield from response.content.read(chunk_size)
                        if not chunk:
                            break
                        file.write(chunk)
                logger.info('Finished downloading {}'.format(filename))
                self.downloaded_items.append(DownloadItem(url, filename))
            else:
                return True

        return filename, (response.status, tuple(response.headers.items()))

    async def start_downloading(self):
        logger.info("Starting download. {} items in queue".format(len(self.urls)))

        async with aiohttp.ClientSession(loop=asyncio.get_event_loop()) as session:
            semaphore = asyncio.Semaphore(5)
            download_tasks = (self.download(url, session, semaphore) for url in self.urls)
            tasks = await asyncio.gather(*download_tasks)
            await self.done_callback(**self.args)

    def on_downloads_complete(self,param):
        asyncio.ensure_future(self.done_callback(**self.args))
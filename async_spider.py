# coding=utf-8
import aiohttp
import traceback
import asyncio
import aiofiles
from fake_useragent import UserAgent
import random


class AsyncSpider:
    def __init__(self, save_path="./img", verify=False, proxies=None):
        self.save_path = save_path
        self.verify = verify
        self.proxies = proxies

    async def download_image(self, sem, url, session, num=0):
        while True:
            headers = {'User-Agent': UserAgent(use_cache_server=False).random, "Connection": "close"}
            try:
                if self.proxies is not None:
                    proxy = random.choice(self.proxies)
                    async with sem:
                        async with session.get(url, headers=headers, verify_ssl=self.verify,
                                               proxy=proxy["http"]) as resp:
                            async with aiofiles.open(self.save_path + "/{}.jpg".format(num), "wb") as fp:
                                await fp.write(await resp.read())
                else:
                    async with sem:
                        async with session.get(url, headers=headers, verify_ssl=self.verify) as resp:
                            async with aiofiles.open(self.save_path + "/{}.jpg".format(num), "wb") as fp:
                                await fp.write(await resp.read())

                    print("%s.jpg saved to %s!" % (num, self.save_path))
                    break
            except Exception as e:
                print("%s.jpg failed to save!" % num)
                traceback.print_exc()
                continue

    async def run(self, url_list, max_worker=8):
        tasks = []
        sem = asyncio.Semaphore(max_worker)  # 限制最大协程数
        async with aiohttp.ClientSession() as session:
            for i, url in enumerate(url_list):
                task = self.download_image(url=url["url"], num=i, sem=sem, session=session)
                task = asyncio.create_task(task)
                tasks.append(task)
            await asyncio.gather(*tasks)

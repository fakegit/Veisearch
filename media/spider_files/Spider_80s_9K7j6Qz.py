import aiohttp
import asyncio
from lxml import etree
import time
import json

class Spider_80s:
    def __init__(self,wd):
        self.wd = wd
        self.url = "http://www.veisearch.com/proxy/"
        self.u_proxy_list = []

    async def fetch_f(self,session):
        async with session.get(self.url) as resp:
            response = await resp.text()
            response = json.loads(response)
            print(response)
        return response

    async def checkproxy(self,session,proxy):
        url = "https://www.80s.la/movie/search/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Host": "www.80s.la",
        }
        data = {
            'search_typeid': 1,
            'skey': self.wd,
            'Input': '搜索',
        }
        try:
            async with session.get(url,headers=headers,data=data,proxy=proxy,timeout=5) as resp:
                if resp.status in [200,201]:
                    self.u_proxy_list.append(proxy)
                    print(proxy + "测试成功————————————————————————————————")
                else:
                    print(proxy+"测试失败")
        except Exception:
            print(proxy+"测试失败")
    async def get_result(self):
        conn = aiohttp.TCPConnector(verify_ssl=False, limit_per_host=5)
        async with aiohttp.ClientSession(connector=conn) as session:
            response = await self.fetch_f(session)
            task = [self.checkproxy(session, proxy) for proxy in response]
            await asyncio.wait(task)
            print(self.u_proxy_list)

    def output_data(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_result())




if __name__ == "__main__":
    start = time.time()
    spider = Spider_80s("斗破苍穹")
    print(spider.output_data())
    print(time.time()-start)
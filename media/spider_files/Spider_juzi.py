import aiohttp
import asyncio
from lxml import etree
import random
import json
class Spider_juzi:

    def __init__(self,wd):
        self.wd = wd
        self.url = "http://juzicili.space/btlist/{}.html".format(self.wd)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        self.detail_list = []
        self.proxy_list = []


    async def prase_n(self,session,response,url):
        print(url+"开始解析")


    async def fetch_n(self,sem,session,url):
       async with sem:
            print("start" + url)
            proxy = self.proxy_list.pop()
            try:
                async with session.get(url, headers=self.headers, proxy=proxy, timeout=5) as resp:
                    response = await resp.text()
                    await self.prase_n(session, response, url)
                    self.proxy_list.append(proxy)
            except:
                print(proxy + "失效")
                await self.fetch_n(sem,session, url)


    async def prase_f2(self,session,response,url):
        html = etree.HTML(response)
        file_url = html.xpath('//ul[@class="mlist"]/li/div[@class="txt1"]/a/@href')
        if len(file_url) == 0:
            await self.fetch_f2(session,url)
        else:
            self.detail_list.extend(file_url)
            print(file_url)
            print("添加完毕")

    async def fetch_f2(self,session,url):
        print("start"+url)
        proxy = self.proxy_list.pop()
        try:
            async with session.get(url,headers=self.headers,proxy=proxy,timeout=5) as resp:
                response = await resp.text()
                await self.prase_f2(session,response,url)
                self.proxy_list.append(proxy)
        except:
            print(proxy+"失效")
            await self.fetch_f2(session,url)


    async def prase_f1(self,session,response):
        html = etree.HTML(response)
        file_url = html.xpath('//ul[@class="mlist"]/li/div[@class="txt1"]/a/@href')
        self.detail_list.extend(file_url)
        page_list = html.xpath('//div[@class="pages"]/a/@href')
        if len(page_list)>5:
            page_list = page_list[:4]
        else:
            page_list = page_list[:-1]

        task = [self.fetch_f2(session,url) for url in page_list]
        await asyncio.wait(task)
        sem = asyncio.Semaphore(20)
        task = [self.fetch_n(sem,session,url) for url in self.detail_list]
        await asyncio.wait(task)



        print(self.detail_list)

    async def fetch_f1(self,session):
        data = {
            "keyword":self.wd
        }
        proxy = self.proxy_list.pop()
        try:
            async with session.post(self.url,data=data,headers=self.headers,proxy=proxy,timeout=5) as resp:
                response = await resp.text()
                await self.prase_f1(session,response)
                self.proxy_list.append(proxy)
        except:
            print(proxy+"失效")
            await self.fetch_f1(session)

    async def get_proxy_list(self,session):
        async with session.get("http://www.veisearch.com/proxy/") as resp:
            response = await resp.text()
            self.proxy_list = json.loads(response)
            print(self.proxy_list)
            return None

    async def get_serach(self):
        conn = aiohttp.TCPConnector(verify_ssl=False, limit=5)
        async with aiohttp.ClientSession(connector=conn) as session:
            await self.get_proxy_list(session)
            response = await self.fetch_f1(session)

    def output_data(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_serach())

if __name__ == "__main__":
    import time
    star_time = time.time()
    spider = Spider_juzi("斗破苍穹")
    spider.output_data()
    print(time.time()-star_time)
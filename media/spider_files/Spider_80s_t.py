import aiohttp
import asyncio
from lxml import etree
import time
import random
import json

class Spider_80s:

    def __init__(self, wd):
        self.MOVIE_LIST = []
        self.wd = wd
        self.proxy_list =[
"http://222.175.171.6:8080",
"http://221.178.232.130:8080",
"http://60.205.202.3:3128",
"http://122.193.247.30:9999",
"http://210.26.64.44:3128",
"http://163.204.241.15:9999",
"http://202.112.51.51:8082",
"http://118.24.185.106:3128",
"http://47.107.175.190:8000",
"http://60.10.2.74:3128",
"http://180.76.149.42:808",
"http://113.121.43.195:9999",
"http://120.234.63.196:3128",
"http://182.92.105.136:3128",
"http://114.55.236.62:3128",
"http://113.124.85.110:9999",
"http://116.196.90.181:3128",
"http://47.106.59.75:3128",
"http://180.76.190.196:3128",
"http://210.22.5.117:3128",
"http://221.226.192.144:10005",
"http://112.109.198.106:3128",
"http://163.204.240.120:9999",
"http://58.220.95.90:10005"]

    async def fetch_f(self, session):
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
        proxy = self.proxy_list.pop()
        print(proxy)
        try:
            async with session.post(url, data=data, headers=headers,proxy=proxy,timeout=5,allow_redirects=False) as response:
                t = await response.text()
                # self.proxy_list.append(proxy)
                return t
        except Exception:
            try:
                print(proxy+"被移除")
                await self.fetch_f(session)
            except:
                await self.fetch_f(session)

    async def fetch_n(self,session, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Origin": "https://www.80s.la",
            "Referer": "https://www.80s.la/movie/search/"

        }
        # async with aiohttp.ClientSession() as session:
        proxy = self.proxy_list.pop()
        try:

            print(proxy)
            async with session.get(url, headers=headers,proxy=proxy,timeout=5,allow_redirects=False) as response:
                rep = await response.text()
                self.proxy_list.append(proxy)
                await self.prase_n(session, rep, url)
        except Exception:
            try:

                print(proxy+"被移除")
                await self.fetch_n(session,url)
            except:
                await self.fetch_n(session, url)

    async def prase_f(self, session,response):
        try:
            html = etree.HTML(response)
            movie_list = html.xpath('//body/div[@id="body"]/div[@class="left"]/div[contains(@class,"clearfix")]/ul/li')
            url_list = []
            for movie in movie_list:
                movie_url = "https://www.80s.la" + movie.xpath('a/@href')[0]
                url_list.append(movie_url)
            if len(url_list)==0:
                response = await self.fetch_f(session)
                return await self.prase_f(session, response)
            return url_list
        except:
            response = await self.fetch_f(session)
            return await self.prase_f(session, response)


    async def prase_n(self, session, response, url):
        try:
            html = etree.HTML(response)
            span = html.xpath('//span[@class="dlb_link_link"]')
            # 如果存在加载按钮，更换url
            if span:
                url = url + '/bd-2'
                response = await self.fetch_n(session,url)
                html = etree.HTML(response)

            movie_list = html.xpath('//form/ul/li')
            for index, movie in enumerate(movie_list):
                if index in (0, len(movie_list) - 1):
                    continue
                else:
                    movie_dict = {}
                    movie_name = movie.xpath('span[contains(@class,"dlname")]/span[1]/a/text()')[0]
                    movie_size = movie.xpath('span[contains(@class,"dlname")]/span[1]/text()')[0].strip()
                    movie_thunder = movie.xpath('span[contains(@class,"dlname")]/span[1]/a/@href')[0]
                    movie_dict["movie_name"] = movie_name
                    movie_dict["movie_size"] = movie_size
                    movie_dict["movie_thunder"] = movie_thunder
                    movie_dict["movie_online_view_address"] = ""
                    movie_dict["source"] = "80s电影网"
                    self.MOVIE_LIST.append(movie_dict)
        except:
            pass


    async def get_proxy_list(self,session):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
        async with session.get("http://www.veisearch.com/proxy/",headers=headers,allow_redirects=False) as resp:
            response = await resp.text()
            self.proxy_list = list(set(json.loads(response)))
            print(self.proxy_list)
            return None
    async def get_search_result(self):
        async with aiohttp.ClientSession() as session:
            # await self.get_proxy_list(session)
            response = await self.fetch_f(session)
            return await self.prase_f(session,response)

    async def get_detail(self,url_list):
        conn = aiohttp.TCPConnector(verify_ssl=False,limit_per_host=5)
        async with aiohttp.ClientSession(connector=conn) as session:
            task = [self.fetch_n(session,url) for url in url_list]
            await asyncio.wait(task)
    def output_data(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        eventloop = asyncio.get_event_loop()
        url_list = eventloop.run_until_complete(self.get_search_result())
        eventloop.run_until_complete(self.get_detail(url_list))
        eventloop.close()
        return self.MOVIE_LIST


if __name__ == "__main__":
    start = time.time()
    spider = Spider_80s("蜘蛛侠")
    print(spider.output_data())
    print(time.time() - start)

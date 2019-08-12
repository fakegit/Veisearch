import threading,requests,json,time
from lxml import etree

class Spider_80s:
    def __init__(self, wd):
        self.MOVIE_LIST = []
        self.wd = wd
        self.proxy_list = ["http://120.234.63.196:3128",
"http://221.178.232.130:8080",
"http://221.122.91.75:9400",
"http://221.122.91.60:80",
"http://221.122.91.61:11013",
"http://60.205.202.3:3128",
"http://47.106.59.75:3128",
"http://106.12.197.44:3128",
"http://120.79.212.174:8000",
"http://202.112.51.51:8082",
"http://221.122.91.34:80",
"http://58.220.95.92:80",
"http://221.122.91.66:10089",
"http://221.122.91.59:10000",
"http://182.92.105.136:3128",
"http://221.122.91.70:10464",
"http://221.122.91.76:9400",
"http://27.102.96.250:3128",
"http://188.166.222.152:3128",
"http://123.206.218.105:80",
"http://221.122.91.74:10101",
"http://42.115.221.58:3128",
"http://42.159.91.248:8080",
"http://114.55.236.62:3128",
"http://60.205.159.195:3128",
"http://218.66.253.144:80"]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
    def get_url_list(self):
        proxy = self.proxy_list.pop()
        proxy_u = {
            "http":proxy
        }
        print(proxy_u)
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
            response = requests.post(url, data=data, headers=self.headers,proxies=proxy_u,allow_redirects=False)
            html = etree.HTML(response.text)
            movie_list = html.xpath('//body/div[@id="body"]/div[@class="left"]/div[contains(@class,"clearfix")]/ul/li')
            url_list = []
            for movie in movie_list:
                movie_url = "https://www.80s.la" + movie.xpath('a/@href')[0]
                url_list.append(movie_url)
            if len(url_list)==0:
                print(proxy + "剔除")
                self.get_url_list()

            return url_list
        except Exception as e:
            print(proxy+"剔除")
            print(repr(e))
            self.get_url_list()

    def get_detail_resp(self,lock,url):
        response = requests.get(url,headers=self.headers)
        html = etree.HTML(response.text)
        span = html.xpath('//span[@class="dlb_link_link"]')
        # 如果存在加载按钮，更换url
        if span:
            url = url + '/bd-2'
            response = requests.get(url, headers=self.headers)
            html = etree.HTML(response.text)

        movie_list = html.xpath('//form/ul/li')
        movie_list_n = []
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
                movie_list_n.append(movie_dict)
        with lock:
            self.MOVIE_LIST.extend(movie_list_n)


    def output_data(self):
        url_list = self.get_url_list()
        import threading
        from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
        thread_pool = ThreadPoolExecutor(max_workers=3)
        lock = threading.Lock()
        all_task = [thread_pool.submit(self.get_detail_resp,lock,url) for url in url_list]
        wait(all_task, return_when=ALL_COMPLETED)
        return self.MOVIE_LIST



if __name__ == "__main__":
    start = time.time()
    spider = Spider_80s("蜘蛛侠")
    print(spider.output_data())
    print(time.time() - start)







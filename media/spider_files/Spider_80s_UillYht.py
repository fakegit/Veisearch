import requests
from lxml import etree
from daili.UserAgents import UA
from random import choice


class Spide_80s:
    """
    80s电影网
    """

    def __init__(self):
        ua = UA()
        self.headers = {
            "User-Agent": choice(ua.useragents["PC"]["Opera"])
        }
        self.url = "https://www.80s.la/"

    def get_url(self):
        print(self.headers)
        response = requests.get(url=self.url, headers=self.headers)
        print(response.text)

    def search(self):
        url = self.url + "movie/search/"
        data = {
            'search_typeid': 1,
            'skey': '火影',
            'Input': '搜索'
        }
        response = requests.post(url=url, data=data, headers=self.headers)
        html = etree.HTML(response.text)
        movie_list=html.xpath('//body/div[@id="body"]/div[@class="left"]/div[@class="clearfix noborder"]/ul/li/a/@href')
        print(type(movie_list))
        for item in movie_list:
            self.detail(item.strip())
    def detail(self,url):
        url = self.url + url[1:]
        print(url)
        response = requests.get(url=url,headers=self.headers)
        html = etree.HTML(response.text)
        movie = html.xpath('//body/div[@id="body"]/div[@class="left"]/div[2]/div[2]/div/div[@id="cpdl2list"]/form/ul/li')
        movie_detail_list = []
        for item in movie[1:-1]:
            size = item.xpath('span[@class="dlname nm"]/span[1]/text()')[0].strip()
            detail = item.xpath('span[@class="dlname nm"]/span[1]/a')[0]
            thunder = detail.xpath('@href')[0]
            name = detail.xpath('text()')[0]
            detail_dict = {
                "电影名":name,
                "大小":size,
                "迅雷链接":thunder
            }
            movie_detail_list.append(detail_dict)
            print(movie_detail_list)
if __name__ == "__main__":
    spide = Spide_80s()
    spide.search()
    # spide.detail()



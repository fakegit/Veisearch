import requests
from lxml import etree


class Spider_80s:
    """
    80s电影网
    """

    def __init__(self,wd):

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        }
        self.url = "https://www.80s.la/movie/search/"
        self.wd = wd
        self.movie_list = []

    def get_search_result(self):
        data = {
            'search_typeid': 1,
            'skey': self.wd,
            'Input': '搜索',
        }
        response = requests.post(self.url,headers=self.headers,data=data)
        html = etree.HTML(response.text)
        movie_list = html.xpath('//body/div[@id="body"]/div[@class="left"]/div[contains(@class,"clearfix")]/ul/li')
        url_list = []
        for movie in movie_list:
            movie_url = "https://www.80s.la"+movie.xpath('a/@href')[0]
            url_list.append(movie_url)

        for url in url_list:
            self.get_movie(url)

    def get_movie(self,url):
        response = requests.get(url,headers=self.headers)
        html = etree.HTML(response.text)
        span = html.xpath('//span[@class="dlb_link_link"]')
        # 如果存在加载按钮，更换url
        if span:
            url = url+'/bd-2'
            response = requests.get(url,headers=self.headers)
            html = etree.HTML(response.text)

        movie_list = html.xpath('//form/ul/li')

        for index,movie in enumerate(movie_list):
            if index in(0,len(movie_list)-1):
                continue
            else:
                movie_dict ={}
                movie_name = movie.xpath('span[contains(@class,"dlname")]/span[1]/a/text()')[0]
                movie_size = movie.xpath('span[contains(@class,"dlname")]/span[1]/text()')[0].strip()
                movie_thunder = movie.xpath('span[contains(@class,"dlname")]/span[1]/a/@href')[0]
                movie_dict["movie_name"] = movie_name
                movie_dict["movie_size"] = movie_size
                movie_dict["movie_thunder"] = movie_thunder

                self.movie_list.append(movie_dict)



    def output_data(self):
        self.get_search_result()

        return self.movie_list
if __name__ == "__main__":
    spide = Spider_80s('复仇者联盟')
    print(spide.output_data())



import requests


class Spider_wbooks:

    def __init__(self,wd):
        self.wd = wd

    def output_data(self):
        data = {
            'search':self.wd
        }
        response = requests.get("http://api.weisapp.top/goods/",params=data)
        return response.text


if __name__ == '__main__':
    spider = Spider_wbooks('宇宙')
    print(spider.output_data())
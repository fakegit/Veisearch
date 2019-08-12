import requests

class Spider_wbooks:
    def __init__(self,wd):
        self.wd = wd
        self.url = "http://api.weisapp.top"

    def output_data(self):
        response = requests.get(self.url)
        return response.text



if __name__ == "__main__":
    spider = Spider_wbooks("wd")
    spider.output_data()
import requests
from lxml import etree
import re
class Proxy_89ip:
    def __init__(self,nums):
        self.nums = nums
        self.url = "http://www.89ip.cn/tqdl.html?num={}&address=&kill_address=&port=&kill_port=&isp=".format(self.nums)
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }

    def main(self):
        response = requests.get(self.url,headers=self.headers)
        html = etree.HTML(response.text)
        detai_data = html.xpath('//div[@class="layui-row layui-col-space15"]/div[1]/div/div/text()')
        proxy_list = [proxy.strip() for proxy in detai_data[:-1] ]
        return proxy_list


if __name__ == "__main__":
    spider = Proxy_89ip(100)
    spider.main()
import requests
from lxml import etree

class Proxy_xici:
    def __init__(self):
        self.url = "https://www.xicidaili.com/wt/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        self.proxy_list = []
    def main(self):
        for i in range(1,6):
            response = requests.get(self.url+str(i),headers=self.headers)
            html = etree.HTML(response.text)
            re = html.xpath('//div[@id="wrapper"]/div[@id="body"]/table[@id="ip_list"]/tr')

            for item in re[1:]:
                proxy_dict = {}
                proxy_dict["re1"] = item.xpath('td[2]/text()')[0]+":"+item.xpath('td[3]/text()')[0]
                proxy_dict["re2"] = item.xpath('td[4]/a/text()')[0]
                proxy_dict["re3"] = item.xpath('td[5]/text()')[0]
                proxy_dict["re4"] = item.xpath('td[6]/text()')[0]
                self.proxy_list.append(proxy_dict)
        return self.proxy_list


if __name__ == "__main__":
    proxy = Proxy_xici()
    print(proxy.main())
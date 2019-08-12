import requests
from lxml import etree
import threading
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED


class Proxy_zdy():
    def __init__(self):
        self.headers ={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Referer": "http://ip.zdaye.com/dayProxy.html",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Requests": "1",
            "Host": "ip.zdaye.com",
            "Cookie": "acw_tc=781bad3015643087183397484e7a2dead91893ee57fad3dfe1a1e951d4399e; ASPSESSIONIDCSDCSBQB=DCJALOKCAAOFMJDLCDGLGMAI; __51cke__=; Hm_lvt_8fd158bb3e69c43ab5dd05882cf0b234=1564308745; ASPSESSIONIDAQCARBSA=FPOPLMLCOPBLIPHAOGPGMALP; __tins__16949115=%7B%22sid%22%3A%201564308745100%2C%20%22vd%22%3A%2014%2C%20%22expires%22%3A%201564311921274%7D; __51laig__=14; Hm_lpvt_8fd158bb3e69c43ab5dd05882cf0b234=1564310121"
        }
        self.proxy_list = []

    def get_url(self):
        response = requests.get("http://ip.zdaye.com/dayProxy.html", headers=self.headers)
        html = etree.HTML(response.text)
        re = html.xpath('//*[@id="J_posts_list"]/div[@class="thread_item"]')
        n_url_list = []
        for item in re[:2]:
            n_url_list.append('http://ip.zdaye.com' + item.xpath('div[@class="thread_content"]/h3/a/@href')[0])
        return n_url_list

    def get_proxy(self,url, lock):
        response = requests.get(url, headers=self.headers)
        html = etree.HTML(response.content.decode("utf-8"))
        re = html.xpath('//*[@id="J_posts_list"]/div[@class="cont"]/text()')
        f_list = []
        for item in re:
            re1, re = item.split("@")
            re2, re = re.split("#[")
            re3, re4 = re.split("]")
            f_list.append(
                {
                    "re1": re1,
                    "re2": re2,
                    "re3": re3,
                    "re4": re4,
                }
            )
        with lock:
            self.proxy_list.extend(f_list)
    def main(self):
        url_list = self.get_url()
        pool = ThreadPoolExecutor(max_workers=5)
        lock = threading.Lock()
        all_task = [pool.submit(self.get_proxy, url, lock) for url in url_list]
        wait(all_task, return_when=ALL_COMPLETED)
        return self.proxy_list




if __name__ =="__main__":
    spider = Proxy_zdy()
    print(spider.main())


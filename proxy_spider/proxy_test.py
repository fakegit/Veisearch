import aiohttp
import asyncio
import time

class Proxytest:
    def __init__(self,proxy_list):
        self.wd = "斗破苍穹"
        self.proxy_list = proxy_list
        self.u_proxy_list = []


    async def checkproxy(self,session,proxy):
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
            async with session.get(url,headers=headers,data=data,proxy=proxy,timeout=5) as resp:
                if resp.status in [200,201]:
                    self.u_proxy_list.append(proxy)
                    print(proxy + "测试成功————————————————————————————————")
                else:
                    print(proxy+"测试失败")
        except Exception:
            print(proxy+"测试失败")
    async def get_test(self):
        conn = aiohttp.TCPConnector(verify_ssl=False, limit_per_host=5)
        async with aiohttp.ClientSession(connector=conn) as session:
            task = [self.checkproxy(session, proxy) for proxy in self.proxy_list]
            await asyncio.wait(task)

    def proxytest(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_test())
        return self.u_proxy_list




if __name__ == "__main__":
    start = time.time()
    proxy_list = ['http://117.191.11.75:8080', 'http://27.208.88.96:8060', 'http://106.14.184.255:80', 'http://140.143.48.49:1080', 'http://223.100.166.3:36945', 'http://106.12.201.174:8080', 'http://163.204.243.179:9999', 'http://163.204.241.125:9999', 'http://125.34.55.64:8060', 'http://60.13.42.19:9999', 'http://163.204.244.104:9999', 'http://115.221.126.26:808', 'http://140.143.142.14:1080', 'http://112.35.56.134:80', 'http://49.51.70.42:1080', 'http://119.131.91.220:9797', 'http://101.132.100.26:80', 'http://111.231.140.109:8888', 'http://60.205.208.120:3128', 'http://103.233.152.140:8080', 'http://120.132.52.137:8888', 'http://121.226.215.132:808', 'http://123.207.17.166:80', 'http://117.191.11.101:80', 'http://27.188.72.54:8060', 'http://218.249.45.162:52316', 'http://60.10.2.74:3128', 'http://117.191.11.103:8080', 'http://47.107.147.168:8000', 'http://123.7.14.63:3128', 'http://47.94.89.87:3128', 'http://117.191.11.105:80', 'http://163.204.240.62:9999', 'http://47.95.10.105:3128', 'http://27.208.94.152:8060', 'http://59.108.125.241:8080', 'http://222.74.237.246:808', 'http://119.51.8.216:8080', 'http://119.179.130.198:8060', 'http://202.112.51.51:8082', 'http://60.10.2.79:3128', 'http://182.35.83.133:9999', 'http://60.9.1.250:80', 'http://49.51.195.24:1080', 'http://110.167.30.50:8060', 'http://112.74.106.205:80', 'http://182.92.105.136:3128', 'http://119.179.141.237:8060', 'http://106.14.82.38:8080', 'http://120.132.53.20:8888', 'http://47.106.196.129:8081', 'http://113.247.252.114:9090', 'http://111.231.94.44:8888', 'http://47.101.156.232:8080', 'http://119.180.143.129:8060', 'http://27.188.62.55:8060', 'http://119.179.179.34:8060', 'http://118.24.182.249:8081', 'http://163.204.244.102:9999', 'http://117.191.11.102:80', 'http://182.35.86.8:9999', 'http://39.137.168.230:80', 'http://117.191.11.79:80', 'http://121.15.254.156:888', 'http://163.204.243.205:9999', 'http://139.196.22.147:80', 'http://182.35.84.154:9999', 'http://193.112.6.56:80', 'http://220.248.229.45:3128', 'http://115.219.172.88:8118', 'http://221.5.80.66:3128', 'http://218.73.138.44:61234', 'http://113.121.188.56:61234', 'http://124.156.108.71:82', 'http://222.222.250.143:8060', 'http://43.254.168.56:53281', 'http://117.191.11.77:80', 'http://60.9.1.81:80', 'http://60.10.2.51:3128', 'http://111.160.121.238:8080', 'http://121.226.74.242:808', 'http://119.179.150.33:8060', 'http://183.157.84.221:8118', 'http://117.191.11.80:8080', 'http://123.207.217.104:1080', 'http://101.4.136.34:80', 'http://37.59.35.174:1080', 'http://118.24.88.66:1080', 'http://183.146.213.198:80', 'http://39.137.69.10:8080', 'http://218.59.139.238:80', 'http://49.51.193.134:1080', 'http://121.40.90.189:8001', 'http://217.182.120.162:1080', 'http://117.186.214.74:9999', 'http://210.22.5.117:3128', 'http://125.109.199.94:808', 'http://117.191.11.107:80', 'http://59.110.212.105:80', 'http://47.112.24.110:80']
    spider = Proxytest(proxy_list)
    print(spider.proxytest())
    print(time.time()-start)
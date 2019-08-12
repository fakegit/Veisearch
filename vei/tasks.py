from __future__ import absolute_import
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from Celery_app.celeryapp import app
from VeiSearch.settings import FROM_ADDR,EMAIL_PASSWORD
from proxy_spider.proxy_zdy import Proxy_zdy
from proxy_spider.proxy_89ip import Proxy_89ip
from proxy_spider.proxy_xici import Proxy_xici
import asyncio
import aiohttp



def proxy_zdy(lock,proxy_obj_list):
    from .models import Proxy
    proxy_spider = Proxy_zdy()
    proxy_list = proxy_spider.main()
    proxy_obj_list_f = []
    for item in proxy_list:
        proxy = Proxy()
        proxy.proxy_ip = item["re1"]
        proxy.proxy_type1 = item["re2"]
        proxy.proxy_type2 = item["re3"]
        proxy.proxy_place = item["re4"][:10]
        proxy_obj_list_f.append(proxy)
    with lock:
        proxy_obj_list.extend(proxy_obj_list_f)

def proxy_89ip(lock,proxy_obj_list):
    from .models import Proxy
    proxy_spider = Proxy_89ip(500)
    proxy_list = proxy_spider.main()
    proxy_obj_list_f = []
    for item in proxy_list:
        proxy = Proxy()
        proxy.proxy_ip = item
        proxy.proxy_place = "未知"
        proxy_obj_list_f.append(proxy)
    with lock:
        proxy_obj_list.extend(proxy_obj_list_f)

def proxy_xici(lock,proxy_obj_list):
    from .models import Proxy
    proxy_spider = Proxy_xici()
    proxy_list = proxy_spider.main()
    proxy_obj_list_f = []
    for item in proxy_list:
        proxy = Proxy()
        proxy.proxy_ip = item["re1"]
        proxy.proxy_type1 = item["re4"]
        proxy.proxy_type2 = item["re3"]
        proxy.proxy_place = item["re2"]
        proxy_obj_list_f.append(proxy)
    proxy_obj_list.extend(proxy_obj_list_f)



@app.task
def getproxy():
    import threading
    from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
    from .models import Proxy
    thread_pool = ThreadPoolExecutor(max_workers=3)
    lock = threading.Lock()
    proxy_obj_list = []
    task1 = thread_pool.submit(proxy_zdy,lock,proxy_obj_list)
    task2 = thread_pool.submit(proxy_89ip,lock,proxy_obj_list)
    task3 = thread_pool.submit(proxy_xici,lock,proxy_obj_list)
    task_list = [task1,task2,task3]
    wait(task_list, return_when=ALL_COMPLETED)
    Proxy.objects.bulk_create(proxy_obj_list)



async def checkproxy(sem,session,proxy_obj,proxy_del_list,proxy_upd_list):
    async with sem:
        url = "https://www.80s.la/movie/search/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Host": "www.80s.la",
        }
        data = {
            'search_typeid': 1,
            'skey': "斗破苍穹",
            'Input': '搜索',
        }
        proxy = "http://"+proxy_obj.proxy_ip
        try:
            async with session.get(url,headers=headers,data=data,proxy=proxy,timeout=5) as resp:
                if resp.status in [200,201]:
                    print(proxy + "测试成功————————————————————————————————")
                    proxy_upd_list.append(proxy_obj.id)
                else:
                    print(proxy+"测试失败")
                    proxy_del_list.append(proxy_obj.id)
        except Exception:
            print(proxy+"测试失败")
            proxy_del_list.append(proxy_obj.id)

async def get_proxy_list():
    from .models import Proxy
    proxy_obj_list = Proxy.objects.all()
    return proxy_obj_list
async def del_proxy(proxy_del_list,proxy_upd_list):
    from .models import Proxy
    Proxy.objects.filter(pk__in=proxy_del_list).delete()
    Proxy.objects.filter(pk__in=proxy_upd_list).update(is_check=True)
async def get_test():
    proxy_del_list = []
    proxy_upd_list = []
    proxy_list = await get_proxy_list()
    conn = aiohttp.TCPConnector(verify_ssl=False, limit_per_host=5)
    async with aiohttp.ClientSession(connector=conn) as session:
        sem = asyncio.Semaphore(30)
        task = [checkproxy(sem,session, proxy_obj,proxy_del_list,proxy_upd_list) for proxy_obj in proxy_list]
        await asyncio.wait(task)
    await del_proxy(proxy_del_list,proxy_upd_list)
    return None





@app.task
def proxytest():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_test())





@app.task
def success_email(to_addr, spider_id):

    def send_email(msg_HTML):
        msg = MIMEText(msg_HTML, 'html', 'utf-8')
        msg['From'] = Header('微搜索<%s>' % FROM_ADDR)
        msg['To'] = Header('菜菜鸡<%s>' % to_addr)
        msg['Subject'] = "审核通过"

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(FROM_ADDR, EMAIL_PASSWORD)
        smtp.sendmail(FROM_ADDR, [to_addr], msg.as_string())

    msg_HTML = """
            <div style="text-align: center;">
    			<h2 style="color: #FF0000;">感谢您的投稿</h2>
    			<h3>您的脚本已经通过审核提交到网站数据库中！</h3>
    			<p>您可以在
    				<a href="https://www.veisearch.com" style="color: #1E90FF; text-decoration: none;">微搜索开发者页面</a>
    				测试您的脚本
    			</p>
    			<p>您的脚本连接如下：
    				<a href="https://www.veisearch.com/script-detail/{}/" style="color: #6495ED;text-decoration: none;">脚本地址</a>
    			</p>
    			<h2>再次感谢您的投稿</h2>
    		</div>
            """.format(spider_id)
    send_email(msg_HTML=msg_HTML)

@app.task
def running_email(to_addr, spider_id):

    def send_email(msg_HTML):
        msg = MIMEText(msg_HTML, 'html', 'utf-8')
        msg['From'] = Header('微搜索<%s>' % FROM_ADDR)
        msg['To'] = Header('菜菜鸡<%s>' % to_addr)
        msg['Subject'] = "恢复运行"

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(FROM_ADDR, EMAIL_PASSWORD)
        smtp.sendmail(FROM_ADDR, [to_addr], msg.as_string())

    msg_HTML = """
            <div style="text-align: center;">
    			<h2 style="color: #FF0000;">感谢您的投稿</h2>
    			<h3>您的脚本已经恢复正常运行！</h3>
    			<p>您可以在
    				<a href="https://www.veisearch.com" style="color: #1E90FF; text-decoration: none;">微搜索开发者页面</a>
    				测试您的脚本
    			</p>
    			<p>您的脚本连接如下：
    				<a href="https://www.veisearch.com/script-detail/{}/" style="color: #6495ED;text-decoration: none;">脚本地址</a>
    			</p>
    			<h2>再次感谢您的投稿</h2>
    		</div>
            """.format(spider_id)
    send_email(msg_HTML=msg_HTML)


@app.task
def stop_eamil(to_addr, spider_id):

    def send_email(msg_HTML):
        msg = MIMEText(msg_HTML, 'html', 'utf-8')
        msg['From'] = Header('微搜索<%s>' % FROM_ADDR)
        msg['To'] = Header('菜菜鸡<%s>' % to_addr)
        msg['Subject'] = "停止运行"

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(FROM_ADDR, EMAIL_PASSWORD)
        smtp.sendmail(FROM_ADDR, [to_addr], msg.as_string())

    msg_HTML = """
                <div style="text-align: center;">
        			<h2 style="color: #FF0000;">您的脚本被停止运行</h2>
        			<h3>我们监测到您上传的脚本在运行过程中出现了大量未知的问题。我们不得已停止了您的脚本在本网站的运行。</h3>
        			<p>您可以在
                				<a href="https://www.veisearch.com" style="color: #1E90FF; text-decoration: none;">微搜索开发者页面</a>查看您的脚本</p>
                		<p>您的脚本连接如下：
                				<a href="https://www.veisearch.com/script-detail/{}/" style="color: #6495ED;text-decoration: none;">脚本地址</a>
                			</p>		

        			<h2>再次感谢您的投稿</h2>
        		</div>
                """.format(spider_id)
    send_email(msg_HTML=msg_HTML)

@app.task
def error_eamil(to_addr, spider_id):

    def send_email(msg_HTML):
        msg = MIMEText(msg_HTML, 'html', 'utf-8')
        msg['From'] = Header('微搜索<%s>' % FROM_ADDR)
        msg['To'] = Header('菜菜鸡<%s>' % to_addr)
        msg['Subject'] = "错误处理"

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(FROM_ADDR, EMAIL_PASSWORD)
        smtp.sendmail(FROM_ADDR, [to_addr], msg.as_string())

    msg_HTML = """
                    <div style="text-align: center;">
            			<h2 style="color: #FF0000;">您的脚本出现了一些问题</h2>
            			<h3>我们监测到您上传的脚本在运行过程中出现了一些未知的问题。我们希望您可以检查一下您的脚本</h3>
            			<p>您可以在
            				<a href="https://www.veisearch.com" style="color: #1E90FF; text-decoration: none;">微搜索开发者页面</a>
            				测试您的脚本
            			</p>
            			<p>您的脚本连接如下：
            				<a href="https://www.veisearch.com/script-detail/{}/" style="color: #6495ED;text-decoration: none;">脚本地址</a>
            			</p>
            			<h2>再次感谢您的投稿</h2>
            		</div>
                    """.format(spider_id)
    send_email(msg_HTML=msg_HTML)

@app.task
def comments_send_email(to_addr, spider_id, comments_addr, comments_name, comments_content):

   def send_email(msg_HTML):
       msg = MIMEText(msg_HTML, 'html', 'utf-8')
       msg['From'] = Header('微搜索<%s>' % FROM_ADDR)
       msg['To'] = Header('菜菜鸡<%s>' % to_addr)
       msg['Subject'] = "脚本评论"

       smtp = smtplib.SMTP('smtp.gmail.com', 587)
       smtp.set_debuglevel(1)
       smtp.ehlo()
       smtp.starttls()
       smtp.login(FROM_ADDR, EMAIL_PASSWORD)
       smtp.sendmail(FROM_ADDR, [to_addr], msg.as_string())

   msg_HTML = """
            <div style="text-align: center;">
    			<h2 style="color: #FF0000;">感谢您的投稿</h2>
    			<h3>您的脚本获得评论一条</h3>
    			<p><b style="color:#32CD32;">{0}</b>对您的脚本做了如下评论:</p>
    			<i style="color:#1E90FF;">{1}</i><br>
    			<p>他的邮箱如下：{2}</p>
    			<p>您可以在
    				<a href="https://www.veisearch.com" style="color: #1E90FF; text-decoration: none;">微搜索开发者页面</a>
    				测试您的脚本或查看相关评论
    			</p>
    			<p>您的脚本连接如下：
    				<a href="https://www.veisearch.com/script-detail/{3}/" style="color: #6495ED;text-decoration: none;">脚本地址</a>
    			</p>
    			<h2>再次感谢您的投稿</h2>
    		</div>
            """.format(comments_name, comments_content, comments_addr, spider_id)
   send_email(msg_HTML=msg_HTML)
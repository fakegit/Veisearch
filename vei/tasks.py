from __future__ import absolute_import
import time
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from celery.utils.log import get_task_logger
from celeryapp import app
from VeiSearch.settings import FROM_ADDR,EMAIL_PASSWORD

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
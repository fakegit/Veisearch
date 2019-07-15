import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class Comments_email:
    def __init__(self, to_addr, spider_id, comments_addr, comments_name, comments_content):
        self.from_addr = "weibw162@gmail.com"
        self.to_addr = to_addr
        self.subject = "微搜索"
        self.password = "v8686521"
        self.spider_id = spider_id
        self.comments_addr = comments_addr
        self.comments_name = comments_name
        self.comments_content = comments_content

    def send_email(self, msg_HTML):
        msg = MIMEText(msg_HTML, 'html', 'utf-8')
        msg['From'] = Header('微搜索<%s>' % self.from_addr)
        msg['To'] = Header('菜菜鸡<%s>' % self.to_addr)
        msg['Subject'] = self.subject

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self.from_addr, self.password)
        smtp.sendmail(self.from_addr, [self.to_addr], msg.as_string())

    def comments_email(self):
        msg_HTML = """
        <div style="text-align: center;">
			<h2 style="color: #FF0000;">感谢您的投稿</h2>
			<h3>您的脚本获得评论一条</h3>
			<p><b>{0}</b>对您的脚本做了如下评论:{1}</p>
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
        """.format(self.comments_name, self.comments_content, self.comments_addr, self.spider_id)
        self.send_email(msg_HTML=msg_HTML)


class Send_email:

    def __init__(self, to_addr, spider_id):
        self.from_addr = "weibw162@gmail.com"
        self.to_addr = to_addr
        self.subject = "微搜索"
        self.password = "v8686521"
        self.spider_id = spider_id

    def send_email(self, msg_HTML):
        msg = MIMEText(msg_HTML, 'html', 'utf-8')
        msg['From'] = Header('微搜索<%s>' % self.from_addr)
        msg['To'] = Header('菜菜鸡<%s>' % self.to_addr)
        msg['Subject'] = self.subject

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self.from_addr, self.password)
        smtp.sendmail(self.from_addr, [self.to_addr], msg.as_string())

    def pass_audit_email(self):
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
        """.format(self.spider_id)
        self.send_email(msg_HTML=msg_HTML)

    def stop_running_eamil(self):
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
        """.format(self.spider_id)
        self.send_email(msg_HTML=msg_HTML)

    def error_eamil(self):
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
                """.format(self.spider_id)
        self.send_email(msg_HTML=msg_HTML)


if __name__ == "__main__":
    # 这里的密码是开启smtp服务时输入的客户端登录授权码，并不是邮箱密码
    # 现在很多邮箱都需要先开启smtp才能这样发送邮件
    mail = Send_email("weibw162@163.com")

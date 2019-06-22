import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class Send_email:

    def __init__(self,to_addr):
        self.from_addr = "weibw162@163.com"
        self.to_addr = to_addr
        self.subject = "微搜索"
        self.password = "Vv86865211"

    def send_email(self,msg_HTML):


        msg = MIMEText(msg_HTML,'html','utf-8')
        msg['From'] = Header('微搜索<%s>' % self.from_addr)
        msg['To'] = Header('菜菜鸡<%s>' % self.to_addr)
        msg['Subject'] = self.subject

        smtp = smtplib.SMTP_SSL('smtp.163.com', 465)
        smtp.set_debuglevel(1)
        smtp.ehlo("smtp.163.com")
        smtp.login(self.from_addr, self.password)
        smtp.sendmail(self.from_addr, [self.to_addr], msg.as_string())

    def pass_audit_email(self):
        msg_HTML = """
        <div style="text-align: center;">
			<h2 style="color: #FF0000;">感谢您的投稿</h2>
			<h3>您的脚本已经通过审核提交到网站数据库中！</h3>
			<p>您可以在
				<a href="https://www.veisearch.com" style="color: #1E90FF; text-decoration: none;">微搜索官网</a>
				测试您的脚本
			</p>
			<p>您的脚本连接如下：
				<a href="https://www.baidu.com" style="color: #6495ED;text-decoration: none;">脚本地址</a>
			</p>
			<h2>再次感谢您的投稿</h2>
		</div>
        """
        self.send_email(msg_HTML=msg_HTML)

    def stop_running_eamil(self):
        msg_HTML = """
        <div style="text-align: center;">
			<h2 style="color: #FF0000;">您的脚本被停止运行</h2>
			<p>您可以在
				<a href="https://www.veisearch.com" style="color: #1E90FF; text-decoration: none;">微搜索官网</a>
				查看您的脚本。
			</p>
			<p>您的脚本出现问题。希望您可以抽出时间查看并修正
			</p>
			<h2>再次感谢您的投稿</h2>
		</div>
        """
        self.send_email(msg_HTML=msg_HTML)

    def error_eamil(self):
        msg_HTML = """
                <div style="text-align: center;">
        			<h2 style="color: #FF0000;">您的脚本出现了一些问题</h2>
        			<h3>我们希望您可以检查一下您的脚本</h3>
        			<p>您可以在
        				<a href="https://www.veisearch.com" style="color: #1E90FF; text-decoration: none;">微搜索官网</a>
        				测试您的脚本
        			</p>
        			<p>您的脚本连接如下：
        				<a href="https://www.baidu.com" style="color: #6495ED;text-decoration: none;">脚本地址</a>
        			</p>
        			<h2>再次感谢您的投稿</h2>
        		</div>
                """
        self.send_email(msg_HTML=msg_HTML)



if __name__ == "__main__":
    # 这里的密码是开启smtp服务时输入的客户端登录授权码，并不是邮箱密码
    # 现在很多邮箱都需要先开启smtp才能这样发送邮件
    mail = Send_email("weibw162@163.com")

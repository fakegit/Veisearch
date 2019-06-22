import random
from datetime import datetime

from django.db import models


# Create your models here.
# 自定义文件存储路径+文件名



class Spider_type(models.Model):
    """
    爬虫类型
    """
    name = models.CharField(verbose_name="类型名", max_length=30, )
    data_format = models.TextField(verbose_name="数据返回格式", max_length=500, )

    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "爬虫类型"
        verbose_name_plural = verbose_name


class Spider(models.Model):
    """
    爬虫详情
    """
    SPIDER_STATUS = (
        ('success','正在运行'),
        ('error','出现问题'),
        ('failed','停止运行')
    )

    name = models.CharField(verbose_name="爬虫名称", max_length=30)
    content = models.FileField(verbose_name="爬虫详情", upload_to='spider_files/')
    function_introduce = models.CharField(verbose_name="功能介绍", default="", max_length=300)
    author = models.CharField(verbose_name="爬虫作者", max_length=30)
    spider_type = models.ForeignKey("Spider_type", verbose_name="爬虫类型", on_delete=models.CASCADE, )
    website_address = models.CharField(verbose_name="爬虫执行网站", max_length=100)
    website_name = models.CharField(verbose_name="网站名称",max_length=100)
    website_img = models.ImageField(verbose_name="网站首页截图",upload_to='website_imgs/',blank=True,null=True)
    author_email = models.CharField(verbose_name="作者邮箱", max_length=30, )
    allowed_email = models.BooleanField(verbose_name="是否允许发送邮件", default=True)
    view_num = models.IntegerField(verbose_name="浏览次数", default=0)
    like_num = models.IntegerField(verbose_name="点赞次数", default=0)
    comments_num = models.IntegerField(verbose_name="评论数", default=0)
    spider_status = models.CharField(verbose_name="爬虫状态",choices=SPIDER_STATUS,default='failed',max_length=30)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.website_img:
            self.website_img = '../static/img/{}.gif'.format(random.randrange(1,8))

        super(Spider, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "爬虫"
        verbose_name_plural = verbose_name

# class Comments(models.Model):
#     spider = models.ForeignKey("Spider", verbose_name="评论对象", on_delete=models.CASCADE,)
#     content = models.TextField(verbose_name="评论内容", max_length=200, )
#     nickname = models.CharField(verbose_name="评论人", max_length=20)
#     comments_email = models.CharField(verbose_name="评论邮箱",max_length=100)
#
#     class Meta:
#         verbose_name = "评论"
#         verbose_name_plural = verbose_name
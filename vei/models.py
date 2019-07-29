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
        ('success', '审核通过'),
        ('running', '正在运行'),
        ('error', '出现问题'),
        ('stop', '停止运行')
    )

    name = models.CharField(verbose_name="爬虫名称", max_length=30)
    content = models.FileField(verbose_name="爬虫详情", upload_to='spider_files/')
    function_introduce = models.CharField(verbose_name="功能介绍", default="", max_length=300)
    author = models.CharField(verbose_name="爬虫作者", max_length=30)
    spider_type = models.ForeignKey("Spider_type", verbose_name="爬虫类型", on_delete=models.CASCADE, )
    website_address = models.CharField(verbose_name="爬虫执行网站", max_length=100)
    website_name = models.CharField(verbose_name="网站名称", max_length=100)
    website_img = models.ImageField(verbose_name="网站首页截图", upload_to='website_imgs/', blank=True, null=True)
    author_email = models.CharField(verbose_name="作者邮箱", max_length=30, )
    allowed_email = models.BooleanField(verbose_name="是否允许发送邮件", default=True)
    view_num = models.IntegerField(verbose_name="浏览次数", default=0)
    like_num = models.IntegerField(verbose_name="点赞次数", default=0)
    comments_num = models.IntegerField(verbose_name="评论数", default=0)
    spider_status = models.CharField(verbose_name="爬虫状态", choices=SPIDER_STATUS, default='stop', max_length=30)
    error_num = models.IntegerField(verbose_name="出错次数", default=0)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    def save(self, *args, **kwargs):
        # 如果用户未上传网站图片
        if not self.website_img:
            self.website_img = '../static/img/{}.gif'.format(random.randrange(1, 8))
        # 如果爬虫脚本出现错误超过50次
        if self.error_num >= 50:
            if self.error_num >= 100:
                self.spider_status = 'stop'
            else:
                self.spider_status = 'error'

        super(Spider, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "爬虫"
        verbose_name_plural = verbose_name


class Comments(models.Model):
    """
    评论
    """
    spider = models.ForeignKey("Spider", verbose_name="评论对象", on_delete=models.CASCADE, )
    content = models.TextField(verbose_name="评论内容", max_length=200, )
    comments_name = models.CharField(verbose_name="评论人", max_length=20)
    comments_email = models.CharField(verbose_name="评论邮箱", max_length=100)
    comments_img = models.ImageField(upload_to='comments_imgs/')

    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name


class Spider_Error(models.Model):
    """
    报错
    """
    spider = models.ForeignKey("Spider", verbose_name="出错爬虫", on_delete=models.CASCADE, )
    error_content = models.CharField(verbose_name="报错内容", max_length=500)

    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    def save(self, *args, **kwargs):
        self.spider.error_num += 1
        # if spider.error_num >= 50:
        #     if spider.error_num >= 100:
        #         spider.spider_status = 'failed'
        #     else:
        #         spider.spider_status = 'error'
        self.spider.save()

        super(Spider_Error, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "脚本报错"
        verbose_name_plural = verbose_name


class Proxy(models.Model):
    """
    代理
    """


    proxy_ip = models.CharField(verbose_name="代理IP", max_length=30)
    proxy_type1 = models.CharField(verbose_name="代理类型",  default="HTTP", max_length=10)
    proxy_type2 = models.CharField(verbose_name="代理类型",  default="未知", max_length=10)
    proxy_place = models.CharField(verbose_name="地区", max_length=100)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "代理"
        verbose_name_plural = verbose_name


class Broadcast(models.Model):
    """
    播报
    """
    cast_content = models.CharField(verbose_name="播报内容", max_length=300)
    is_used = models.BooleanField(verbose_name="是否启用", default=True)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    def save(self, *args, **kwargs):
        Broadcast.objects.update(is_used=False)
        super(Broadcast, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "播报"
        verbose_name_plural = verbose_name


class Shuffling(models.Model):
    """
    轮播图
    """
    img = models.ImageField(verbose_name="轮播图", upload_to='shuffling_imgs/')
    is_used = models.BooleanField(verbose_name="是否启用", default=True)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

class Search(models.Model):
    """
    用户搜索记录
    """
    user_ip = models.CharField(verbose_name="用户ip",max_length=100)
    search_type = models.ForeignKey("Spider_type",verbose_name="搜索类型",on_delete=models.CASCADE)
    wd = models.CharField(verbose_name="搜索词条",max_length=100)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    def __str__(self):
        return self.wd

    class Meta:
        verbose_name = "用户搜索记录"
        verbose_name_plural = verbose_name


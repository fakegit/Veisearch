import importlib
import json
import random
from django.shortcuts import render,HttpResponse

from .models import Spider_type, Spider,Comments,Spider_Error



def index(request):
    """
    首页
    :param request:
    :return:
    """
    spider_list = Spider.objects.all()[:8]

    return render(request, 'index.html', {'spider_list': spider_list})


def upload(request):
    """
    上传页
    :param request:
    :return:
    """
    spider_type_list = Spider_type.objects.all()

    return render(request, 'upload.html', {'spider_type_list': spider_type_list})


def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        website_img = request.FILES.get('website_img')

        script_type = request.POST.get('script-type')
        website_address = request.POST.get('website_address')
        website_name = request.POST.get('website_name')
        author = request.POST.get('author')
        author_email = request.POST.get('author_email')
        allowed_email = request.POST.get('allowed_email')
        function_introduce = request.POST.get('function_introduce')

        spider = Spider()
        spider.website_img = website_img
        spider.website_name = website_name
        spider.name = file.name
        spider.content = file
        spider.function_introduce = function_introduce
        spider.author = author
        spider.spider_type = Spider_type.objects.get(name=script_type)
        spider.website_address = website_address
        spider.author_email = author_email
        if allowed_email == "on":
            spider.allowed_email = True
        else:
            spider.allowed_email = False
        # spider.save()

        spider.save()

    return render(request, 'upload_success.html')


def scriptdetail(request, script_id):
    """
    脚本详情页
    :param request:
    :param script_id:
    :return:
    """
    spider_content = ''
    spider_type_list = Spider_type.objects.all()
    spider = Spider.objects.filter(pk=script_id)
    if spider.exists():
        spider = spider[0]
        spider.view_num +=1
        spider.save()
        spider_content = spider.content.read().decode('utf-8').lstrip()

    # 获取评论
    comments_list = Comments.objects.filter(spider=spider)

    context = {
        'spider_type_list': spider_type_list,
        'spider': spider,
        'spider_content':spider_content,
        'comments_list':comments_list,
    }
    # if request.META.has_key('HTTP_X_FORWARDED_FOR'):
    #     ip = request.META['HTTP_X_FORWARDED_FOR']
    # else:
    #     ip = request.META['REMOTE_ADDR']
    # print(request.META)



    return render(request, 'scriptdetail.html', context)

def script_test(request,script_id):
    """
    脚本测试
    :param request:
    :return:
    """
    wd = ''
    if request.is_ajax():
        wd = request.POST.get('wd')
    spider = Spider.objects.filter(pk=script_id)
    if spider.exists():
        spider = spider[0]
    model = importlib.import_module('media.spider_files.'+spider.name[:-3])  # 根据"auth.my_auth"导入my_auth模块
    obj = getattr(model, spider.name[:-3])(wd)  # 反射并实例化
    result = obj.output_data()

    return HttpResponse(json.dumps(result))

def comments(request,script_id):
    """
    评论
    :param request:
    :param script_id:
    :return:
    """
    spider = Spider.objects.filter(pk=script_id)
    if spider.exists():
        spider = spider[0]

    comments_name = ''
    comments_content =''
    comments_email = ''
    if request.is_ajax():
        comments_name=request.POST.get('comments_name')
        comments_content = request.POST.get('comments_content')
        comments_email = request.POST.get('comments_email')

    comments = Comments()
    comments.spider = spider
    comments.comments_email = comments_email
    comments.comments_name = comments_name
    comments.content = comments_content
    comments.comments_img ='../static/img/{}.gif'.format(random.randrange(1,8))
    comments.save()

    new_comments = {}
    new_comments["comments_name"] = comments.comments_name
    new_comments["comments_content"] = comments.content = comments_content
    new_comments["comments_img"] = str(comments.comments_img)
    new_comments["add_time"] = str(comments.add_time.year)+'年'+str(comments.add_time.month)+'月'+str(comments.add_time.day)+'日 '+str(comments.add_time.hour)+':'+str(comments.add_time.minute)

    return HttpResponse(json.dumps(new_comments))

def script_list(request,script_type_id):
    """
    脚本列表页
    :param request:
    :param script_type_id:
    :return:
    """
    spider_type_list = Spider_type.objects.all()
    this_spider_type = Spider_type.objects.filter(pk=script_type_id)
    spider_list = []
    if this_spider_type.exists():
        this_spider_type = this_spider_type[0]
        spider_list = Spider.objects.filter(spider_type=this_spider_type)

    context = {
        "spider_type_list":spider_type_list,
        "spider_list":spider_list,
        "this_spider_type":this_spider_type,
    }

    return render(request,'scriptlist.html',context=context)

def veisearch(request):
    return render(request,'veisearch.html')

def search(request):
    wd = ''
    if request.method =="POST":
        wd = request.body.decode("utf-8")[7:-2]
    print(type(wd))
    print(wd)
    result = []
    spider_list = Spider.objects.all()

    for spider in spider_list:

        model = importlib.import_module('media.spider_files.' + spider.name[:-3])
        obj = getattr(model, spider.name[:-3])(wd)
        result = obj.output_data()
        print(result)


    return HttpResponse(json.dumps(result))
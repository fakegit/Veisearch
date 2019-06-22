import importlib
import json

from django.shortcuts import render,HttpResponse

from .models import Spider_type, Spider



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

    context = {
        'spider_type_list': spider_type_list,
        'spider': spider,
        'spider_content':spider_content,
    }

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


import importlib
import json
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.shortcuts import render, HttpResponse

from .models import Spider_type, Spider, Comments, Spider_Error, Proxy, Broadcast, Shuffling
from .tasks import comments_send_email

def index(request):
    """
    首页
    :param request:
    :return:
    """
    broadcast = Broadcast.objects.filter(is_used=True)[0]
    shuffling_list = Shuffling.objects.filter(is_used=True)[:6]
    spider_list = Spider.objects.all().order_by("-add_time")
    pack_list = []
    with open(r'.\requirements.txt') as f:
        line_list = f.readlines()
        for line in line_list:
            k, v = line.split("==")
            pack_list.append({"pack_name": k, "pack_ver": v.strip()})

    comments_list = Comments.objects.order_by("-add_time")
    proxy_list = Proxy.objects.order_by("-add_time")[:20]

    context = {
        "broadcast": broadcast,
        "shuffling_list": shuffling_list,
        "spider_show_list": spider_list[:8],
        "spider_count": len(spider_list),
        "spider_list": spider_list,
        "pack_list": pack_list,
        "comments_list": comments_list[:20],
        "proxy_list": proxy_list,
        "comments_count":len(comments_list),
    }

    return render(request, 'index.html', context)


def upload(request):
    """
    上传页
    :param request:
    :return:
    """
    spider_type_list = Spider_type.objects.all()
    spider_list = Spider.objects.all()
    pack_list = []
    with open(r'.\requirements.txt') as f:
        line_list = f.readlines()
        for line in line_list:
            k, v = line.split("==")
            pack_list.append({"pack_name": k, "pack_ver": v.strip()})
    comments_list = Comments.objects.order_by("-add_time")[:20]
    proxy_list = Proxy.objects.order_by("-add_time")[:20]
    context = {
        "spider_count": len(spider_list),
        "spider_list": spider_list,
        "pack_list": pack_list,
        "comments_list": comments_list,
        "proxy_list": proxy_list,
        'spider_type_list': spider_type_list

    }

    return render(request, 'upload.html', context)


def upload_file(request):
    if request.is_ajax():
        vercode_session = request.session["vercode"]
        vercode_content = request.POST.get('vercode')
        print(vercode_content,vercode_session)
        if vercode_session != vercode_content:
            return HttpResponse("False")
        else:
            file = request.FILES.get('script_file')
            website_img = request.FILES.get('website_img')
            script_type = request.POST.get('script_type')
            website_address = request.POST.get('website_address')
            website_name = request.POST.get('website_name')
            author = request.POST.get('author')
            author_email = request.POST.get('author_email')
            allowed_email = request.POST.get('checkbox')
            function_introduce = request.POST.get('function_introduce')

            spider = Spider()
            spider.website_img = website_img
            spider.website_name = website_name
            spider.name = file.name
            spider.content = file
            spider.function_introduce = function_introduce
            spider.author = author
            spider.spider_type = Spider_type.objects.get(pk=script_type)
            spider.website_address = website_address
            spider.author_email = author_email
            if allowed_email == "true":
                spider.allowed_email = True
            else:
                spider.allowed_email = False
            spider.save()
            return HttpResponse("True")


def upload_success(request):
    return render(request,"upload_success.html")



def scriptdetail(request, script_id):
    """
    脚本详情页
    """
    like_list = []
    try:
        like_list = request.session["like_list"]
    except KeyError:
        pass

    if script_id in like_list:
        like = True
    else:
        like = False
    spider_content = ''
    spider_type_list = Spider_type.objects.all()
    spider = Spider.objects.filter(pk=script_id)
    spider_list = Spider.objects.all()
    proxy_list = Proxy.objects.order_by("-add_time")[:20]
    if spider.exists():
        spider = spider[0]
        spider.view_num += 1
        spider.save()
        spider_content = spider.content.read().decode('utf-8').lstrip()

    # 获取评论
    comments_list = Comments.objects.filter(spider=spider)

    context = {
        "spider_list": spider_list,
        "proxy_list": proxy_list,
        'spider_type_list': spider_type_list,
        'spider': spider,
        'spider_content': spider_content,
        'comments_list': comments_list,
        "like": like
    }
    # if request.META.has_key('HTTP_X_FORWARDED_FOR'):
    #     ip = request.META['HTTP_X_FORWARDED_FOR']
    # else:
    #     ip = request.META['REMOTE_ADDR']
    # print(request.META)

    return render(request, 'scriptdetail.html', context)


def script_test(request, script_id):
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
    model = importlib.import_module('media.spider_files.' + spider.name[:-3])  # 根据"auth.my_auth"导入my_auth模块
    obj = getattr(model, spider.name[:-3])(wd)  # 反射并实例化
    result = obj.output_data()
    # result = "测试成功"

    return HttpResponse(json.dumps(result))


def comments(request, script_id):
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
    comments_content = ''
    comments_email = ''
    if request.is_ajax():
        comments_name = request.POST.get('comments_name')
        comments_content = request.POST.get('comments_content')
        comments_email = request.POST.get('comments_email')

    comments = Comments()
    comments.spider = spider
    comments.comments_email = comments_email
    comments.comments_name = comments_name
    comments.content = comments_content
    comments.comments_img = '../static/img/{}.gif'.format(random.randrange(1, 8))
    comments.save()
    spider.comments_num += 1
    spider.save()

    # 发送邮件
    if spider.allowed_email:
        comments_send_email.delay(to_addr=spider.author_email,spider_id=spider.id,comments_addr=comments_email,comments_name=comments_name,comments_content=comments_content)

    new_comments = {}
    new_comments["comments_name"] = comments.comments_name
    new_comments["comments_content"] = comments.content = comments_content
    new_comments["comments_img"] = str(comments.comments_img)
    new_comments["add_time"] = str(comments.add_time.year) + '年' + str(comments.add_time.month) + '月' + str(
        comments.add_time.day) + '日 ' + str(comments.add_time.hour) + ':' + str(comments.add_time.minute)

    return HttpResponse(json.dumps(new_comments))


def like(request, script_id):
    like_list = []
    try:
        like_list = request.session["like_list"]
    except KeyError:
        pass
    if script_id in like_list:
        return HttpResponse("like_False")
    else:
        like_list.append(script_id)
        request.session["like_list"] = like_list
        spider = Spider.objects.get(pk=script_id)
        spider.like_num += 1
        spider.save()
        return HttpResponse("like_True")


def script_list(request, script_type_id):
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
    comments_list = Comments.objects.order_by("-add_time")[:20]
    proxy_list = Proxy.objects.order_by("-add_time")[:20]
    context = {
        "spider_type_list": spider_type_list,
        "spider_list": spider_list,
        "this_spider_type": this_spider_type,
        "comments_list": comments_list,
        "proxy_list": proxy_list,
    }

    return render(request, 'scriptlist.html', context=context)


def getvercode(request):
    # 获取随机色值
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 比较适合作背景色的色值
    background_color_list = [
        (240, 255, 240),
        (255, 255, 210),
        (255, 248, 238),
        (225, 255, 255),
        (238, 232, 170),
    ]
    # 新建一个图像
    img_obj = Image.new(
        "RGB",
        (100, 27),
        random.choice(background_color_list)
    )
    # 画笔
    draw_obj = ImageDraw.Draw(img_obj)
    # 字体
    font_obj = ImageFont.truetype("static/font/calibri.ttf", 28)
    vercode_list = []
    ver = "abcdefjhjklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ1234567890"
    for i in range(4):
        ver_item = random.choice(ver)
        vercode_list.append(ver_item)
        draw_obj.text((10 + 20 * i, 0), text=ver_item, fill=get_random_color(), font=font_obj)
    # 将验证码信息保存到session中
    request.session["vercode"] = "".join(vercode_list)
    # 加干扰
    width = 100
    height = 27
    # 干扰线
    for i in range(4):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    # 干扰点
    for i in range(40):
        draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # 将验证码存入内存中
    io_obj = BytesIO()
    img_obj.save(io_obj, "png")
    data = io_obj.getvalue()
    return HttpResponse(data)




def veisearch(request):
    return render(request, 'veisearch.html')


def search(request):
    wd = ''
    if request.method == "POST":
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

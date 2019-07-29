import importlib
import json
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.shortcuts import render, HttpResponse
from django.db.models import Sum, Count
from .models import Spider_type, Spider, Comments, Spider_Error, Proxy, Broadcast, Shuffling, Search
from .tasks import comments_send_email


def index(request):
    """
    首页
    """
    if "broadcast" in request.session:
        broadcast = request.session["broadcast"]
    else:
        broadcast = Broadcast.objects.filter(is_used=True).first()
        request.session["broadcast"] = broadcast

    if "shuffling_list" in request.session:
        shuffling_list = request.session["shuffling_list"]
    else:
        shuffling_list = Shuffling.objects.filter(is_used=True)[:6]
        request.session["shuffling_list"] = shuffling_list

    if "spider_list" in request.session:
        spider_list = request.session["spider_list"]
    else:
        spider_list = Spider.objects.all().order_by("-add_time")
        request.session["spider_list"] = spider_list

    if "pack_list" in request.session:
        pack_list = request.session["pack_list"]
    else:
        pack_list = []
        with open(r'.\requirements.txt') as f:
            line_list = f.readlines()
            for line in line_list:
                k, v = line.split("==")
                pack_list.append({"pack_name": k, "pack_ver": v.strip()})
        request.session["pack_list"] = pack_list

    if "proxy_list" in request.session:
        proxy_list = request.session["proxy_list"]
        proxy_count = request.session["proxy_count"]
    else:
        proxy_list = Proxy.objects.all()
        proxy_count = proxy_list.count()
        proxy_list = proxy_list[:60]
        request.session["proxy_count"] = proxy_count
        request.session["proxy_list"] = proxy_list

    if "comments_list" in request.session:
        comments_list = request.session["comments_list"]
    else:
        comments_list = Comments.objects.order_by("-add_time")[:30]
        request.session["comments_list"] = comments_list
    context = {
        "broadcast": broadcast,
        "shuffling_list": shuffling_list,
        "spider_show_list": spider_list[:8],
        "spider_count": len(spider_list),
        "spider_list": spider_list,
        "pack_list": pack_list,
        "pack_list_count": len(pack_list),
        "comments_list": comments_list,
        "proxy_list": proxy_list,
        "proxy_count":proxy_count,
        "comments_count": len(comments_list),
    }

    return render(request, 'index.html', context)


def upload(request):
    """
    上传页
    :param request:
    :return:
    """
    if "spider_type_list" in request.session:
        spider_type_list = request.session["spider_type_list"]
    else:
        spider_type_list = Spider_type.objects.all()
        request.session["spider_type_list"] = spider_type_list

    if "spider_list" in request.session:
        spider_list = request.session["spider_list"]
    else:
        spider_list = Spider.objects.all().order_by("-add_time")
        request.session["spider_list"] = spider_list

    if "pack_list" in request.session:
        pack_list = request.session["pack_list"]
    else:
        pack_list = []
        with open(r'.\requirements.txt') as f:
            line_list = f.readlines()
            for line in line_list:
                k, v = line.split("==")
                pack_list.append({"pack_name": k, "pack_ver": v.strip()})
        request.session["pack_list"] = pack_list

    if "proxy_list" in request.session:
        proxy_list = request.session["proxy_list"]
    else:
        proxy_list = Proxy.objects.order_by("-add_time")[:60]
        request.session["proxy_list"] = proxy_list

    if "comments_list" in request.session:
        comments_list = request.session["comments_list"]
    else:
        comments_list = Comments.objects.order_by("-add_time")[:30]
        request.session["comments_list"] = comments_list

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
    if "spider_list" in request.session:
        spider_list = request.session["spider_list"]
    else:
        spider_list = Spider.objects.all().order_by("-add_time")
        request.session["spider_list"] = spider_list

    if "proxy_list" in request.session:
        proxy_list = request.session["proxy_list"]
    else:
        proxy_list = Proxy.objects.order_by("-add_time")[:60]
        request.session["proxy_list"] = proxy_list

    if "comments_list" in request.session:
        comments_list = request.session["comments_list"]
    else:
        comments_list = Comments.objects.order_by("-add_time")[:30]
        request.session["comments_list"] = comments_list
    context ={
        "spider_list": spider_list,
        "comments_list": comments_list,
        "proxy_list": proxy_list,
    }
    return render(request, "upload_success.html",context=context)


def scriptdetail(request, script_id):
    """
    脚本详情页
    """
    like_list = []
    if "like_list" in request.session:
        like_list = request.session["like_list"]
    if script_id in like_list:
        like = True
    else:
        like = False

    if "spider_type_list" in request.session:
        spider_type_list = request.session["spider_type_list"]
    else:
        spider_type_list = Spider_type.objects.all()
        request.session["spider_type_list"] = spider_type_list

    if "spider_list" in request.session:
        spider_list = request.session["spider_list"]
    else:
        spider_list = Spider.objects.all().order_by("-add_time")
        request.session["spider_list"] = spider_list
    if "proxy_list" in request.session:
        proxy_list = request.session["proxy_list"]
    else:
        proxy_list = Proxy.objects.order_by("-add_time")[:60]
        request.session["proxy_list"] = proxy_list

    spider = Spider.objects.filter(pk=script_id)
    spider_content = ''
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
    spider = Spider.objects.filter(pk=script_id).first()
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
    spider = Spider.objects.filter(pk=script_id).first()
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
        comments_send_email.delay(to_addr=spider.author_email, spider_id=spider.id, comments_addr=comments_email,
                                  comments_name=comments_name, comments_content=comments_content)

    new_comments = {}
    new_comments["comments_name"] = comments.comments_name
    new_comments["comments_content"] = comments.content = comments_content
    new_comments["comments_img"] = str(comments.comments_img)
    new_comments["add_time"] = str(comments.add_time.year) + '年' + str(comments.add_time.month) + '月' + str(
        comments.add_time.day) + '日 ' + str(comments.add_time.hour) + ':' + str(comments.add_time.minute)

    return HttpResponse(json.dumps(new_comments))


def like(request, script_id):
    like_list = []
    if "like_list" in request.session:
        like_list = request.session["like_list"]
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
    """
    if "spider_type_list" in request.session:
        spider_type_list = request.session["spider_type_list"]
    else:
        spider_type_list = Spider_type.objects.all()
        request.session["spider_type_list"] = spider_type_list
    this_spider_type = Spider_type.objects.filter(pk=script_type_id).first()

    spider_list_key = "spider_list"+str(this_spider_type.id)
    if spider_list_key in request.session:
        spider_list = request.session[spider_list_key]
    else:
        spider_list = Spider.objects.filter(spider_type=this_spider_type)
        request.session[spider_list_key] = spider_list

    if "proxy_list" in request.session:
        proxy_list = request.session["proxy_list"]
    else:
        proxy_list = Proxy.objects.order_by("-add_time")[:20]
        request.session["proxy_list"] = proxy_list

    if "comments_list" in request.session:
        comments_list = request.session["comments_list"]
    else:
        comments_list = Comments.objects.order_by("-add_time")[:30]
        request.session["comments_list"] = comments_list

    context = {
        "spider_type_list": spider_type_list,
        "spider_list": spider_list,
        "this_spider_type": this_spider_type,
        "comments_list": comments_list,
        "proxy_list": proxy_list,
    }

    return render(request, 'scriptlist.html', context=context)

def createvercode():
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
    vercode = "".join(vercode_list)
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
    return (vercode,data)


def getvercode(request):
    vercode,data = createvercode()
    request.session["vercode"] = vercode
    return HttpResponse(data)


def veisearch(request):
    if "hotsearch_list" in request.session:
        hotsearch_list = request.session["hotsearch_list"]
    else:
        hotsearch_list = Search.objects.values("wd").annotate(wd_count=Count("wd")).order_by("-wd_count")[:10]
        request.session["hotsearch_list"] = hotsearch_list

    if "search_records" in request.session:
        search_records = request.session["search_records"]
    else:
        search_records = []
    context = {
        "hotsearch_list": hotsearch_list,
        "search_records":search_records,
    }

    return render(request, 'veisearch.html', context=context)


def run(wd, spider, f_result, lock):
    try:
        model = importlib.import_module('media.spider_files.' + spider.name[:-3])
        obj = getattr(model, spider.name[:-3])(wd)
        result = obj.output_data()
        with lock:
            f_result.extend(result)
    except Exception as e:
        spider_error = Spider_Error()
        spider_error.spider = spider
        spider_error.error_content = repr(e)
        spider_error.save()


def run_spider(id, wd, f_result):
    import threading
    from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
    thread_pool = ThreadPoolExecutor(max_workers=3)
    lock = threading.Lock()
    spider_type = Spider_type.objects.filter(pk=id).first()
    spider_list = Spider.objects.filter(spider_type=spider_type).exclude(spider_status="stop")
    all_task = [thread_pool.submit(run, wd, spider, f_result, lock) for spider in spider_list]
    wait(all_task, return_when=ALL_COMPLETED)
    return f_result


def search(request):
    wd = ''
    cate = ''
    f_result = []
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    if request.method == "POST":
        wd = request.POST.get("wd")
        cate = request.POST.get("cate")
    if "search_records" in request.session:
        search_records = request.session["search_records"]
        if wd not in search_records:
            search_records.append(wd)
            if len(search_records) > 10:
                search_records =  search_records[1:]
            request.session["search_records"] = search_records
    else:
        search_records = [wd]
        request.session["search_records"] = search_records
    try:
        f_result = run_spider(int(cate), wd, f_result)
        user_search = Search()
        user_search.user_ip = ip
        user_search.wd = wd
        user_search.search_type = Spider_type.objects.filter(pk=int(cate)).first()
        user_search.save()
    except:
        pass

    return HttpResponse(json.dumps(f_result))

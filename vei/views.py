from django.shortcuts import render

from .models import Spider_type, Spider


def index(request):
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
        name = request.POST.get('file')
        script_type = request.POST.get('script-type')
        website_address = request.POST.get('website_address')
        author = request.POST.get('author')
        author_email = request.POST.get('author_email')
        allowed_email = request.POST.get('allowed_email')
        function_introduce = request.POST.get('function_introduce')

        spider = Spider()
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

from django.contrib import admin

from .models import Spider_type, Spider,Comments,Spider_Error,Proxy,Broadcast,Shuffling,Search


from .tasks import success_email,running_email,stop_eamil,error_eamil

class Spider_typeAdmin(admin.ModelAdmin):
    list_display = ['name', 'data_format', 'add_time']


class SpiderAdmin(admin.ModelAdmin):
    list_display = ['pk','name', 'content', 'author', 'Spider_type', 'website_address', 'website_name',
                    'author_email', 'allowed_email', 'view_num', 'like_num', 'comments_num', 'error_num',
                    'spider_status', 'add_time']

    def Spider_type(self, obj):
        return "%s" % (obj.spider_type.name)

    def save_model(self, request, obj, form, change):
        spider = Spider.objects.filter(pk=obj.id)[0]
        if spider.spider_status != obj.spider_status:
            if obj.spider_status == "success":
                success_email.delay(obj.author_email,obj.id)
            elif obj.spider_status == "error":
                error_eamil.delay(obj.author_email,obj.id)
            elif obj.spider_status == "stop":
                stop_eamil.delay(obj.author_email,obj.id)
            elif obj.spider_status == "running":
                running_email.delay(obj.author_email,obj.id)
        obj.save()


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['spider','content','comments_name','comments_email','add_time',]

class ErrorAdmin(admin.ModelAdmin):
    list_display = ['spider','error_content','add_time']

class ProxyAdmin(admin.ModelAdmin):
    list_display = ["pk","proxy_ip","is_check","proxy_type1","proxy_type2","add_time"]

class BroadcastAdmin(admin.ModelAdmin):
    list_display = ["pk","cast_content","is_used","add_time"]

class ShufflingAdmin(admin.ModelAdmin):
    list_display = ["pk","img","is_used","add_time"]

class SearchAdmin(admin.ModelAdmin):
    list_display = ["pk","user_ip","search_type","wd","add_time"]

admin.site.register(Spider_type, Spider_typeAdmin)
admin.site.register(Spider, SpiderAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Spider_Error, ErrorAdmin)
admin.site.register(Proxy, ProxyAdmin)
admin.site.register(Broadcast, BroadcastAdmin)
admin.site.register(Shuffling, ShufflingAdmin)
admin.site.register(Search, SearchAdmin)



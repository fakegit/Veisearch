from django.contrib import admin

from .models import Spider_type, Spider,Comments,Spider_Error,Proxy,Broadcast,Shuffling

from Email.audit_statusmod_mail import Send_email


class Spider_typeAdmin(admin.ModelAdmin):
    list_display = ['name', 'data_format', 'add_time']


class SpiderAdmin(admin.ModelAdmin):
    list_display = ['pk','name', 'content', 'author', 'Spider_type', 'website_address', 'website_name',
                    'author_email', 'allowed_email', 'view_num', 'like_num', 'comments_num', 'comments_num',
                    'spider_status', 'add_time']

    def Spider_type(self, obj):
        return "%s" % (obj.spider_type.name)

    def save_model(self, request, obj, form, change):
        spider = Spider.objects.filter(pk=obj.id)[0]
        if spider.spider_status != obj.spider_status:
            mail = Send_email(obj.author_email,obj.id)
            if obj.spider_status == "success":
                mail.pass_audit_email()
            elif obj.spider_status == "error":
                mail.error_eamil()
            elif obj.spider_status == "failed":
                mail.stop_running_eamil()
        obj.save()


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['spider','content','comments_name','comments_email','add_time',]

class ErrorAdmin(admin.ModelAdmin):
    list_display = ['spider','Error_content','add_time']

class ProxyAdmin(admin.ModelAdmin):
    list_display = ["pk","proxy_ip","proxy_type1","proxy_type2","add_time"]

class BroadcastAdmin(admin.ModelAdmin):
    list_display = ["pk","cast_content","is_used","add_time"]

class ShufflingAdmin(admin.ModelAdmin):
    list_display = ["pk","img","is_used","add_time"]


admin.site.register(Spider_type, Spider_typeAdmin)
admin.site.register(Spider, SpiderAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Spider_Error, ErrorAdmin)
admin.site.register(Proxy, ProxyAdmin)
admin.site.register(Broadcast, BroadcastAdmin)
admin.site.register(Shuffling, ShufflingAdmin)


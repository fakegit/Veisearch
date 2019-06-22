from django.contrib import admin

from .models import Spider_type, Spider

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
            mail = Send_email(obj.author_email)
            if obj.spider_status == "success":
                mail.pass_audit_email()
            elif obj.spider_status == "error":
                mail.error_eamil()
            elif obj.spider_status == "failed":
                mail.stop_running_eamil()
        obj.save()


admin.site.register(Spider_type, Spider_typeAdmin)
admin.site.register(Spider, SpiderAdmin)

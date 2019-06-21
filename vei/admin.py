from django.contrib import admin

from .models import Spider_type,Spider


class Spider_typeAdmin(admin.ModelAdmin):
    list_display = ['name','data_format','add_time']

class SpiderAdmin(admin.ModelAdmin):
    list_display = ['name','content','function_introduce','author','Spider_type','website_address','author_email',
                    'allowed_email','view_num','like_num','comments_num','comments_num','spider_status','add_time']


    def Spider_type(self,obj):
        return "%s"%(obj.spider_type.name)

admin.site.register(Spider_type, Spider_typeAdmin)
admin.site.register(Spider,SpiderAdmin)
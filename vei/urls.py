from django.urls import path,re_path

from . import views

urlpatterns = [
    path('',views.veisearch),
    path('search/',views.search),
    path('pro/',views.index),
    path('upload-script/',views.upload),
    path('upload/', views.upload_file),
    path('upload-success/',views.upload_success),
    path('script-detail/<int:script_id>/',views.scriptdetail),
    path('script-test/<int:script_id>/',views.script_test),
    path('comments/<int:script_id>/',views.comments),
    path('like/<int:script_id>/',views.like),
    path('script-list/<int:script_type_id>/',views.script_list),
    path('vercode/',views.getvercode),
    path('proxy/',views.getproxy),

]
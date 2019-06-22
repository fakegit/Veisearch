from django.urls import path,re_path

from . import views

urlpatterns = [
    path('',views.index),
    path('upload/',views.upload),
    path('upload-script/', views.upload_file),
    path('scriptdetail/<int:script_id>/',views.scriptdetail),
    path('script-test/<int:script_id>',views.script_test),

]
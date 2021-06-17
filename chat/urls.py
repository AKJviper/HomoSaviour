from django.urls import  re_path

from .views import ChatDelete, Chatlistall, ThreadDetailView,  ChatListView, ThreadView, InboxView, ThreadListView, Chatimgupload

app_name = 'chat'
urlpatterns = [
    re_path(r"^inbox/(?P<username>[\w.@+-]+)/$", InboxView.as_view()),
    re_path(r"^messages/(?P<username>[\w.@+-]+)/$", ThreadView.as_view()),
    re_path(r"^chatlist/(?P<username>[\w.@+-]+)/$", ChatListView.as_view()),
    re_path(r"^chatlist30/(?P<username>[\w.@+-]+)/$", Chatlistall.as_view()),
    re_path(r"^deletechat/(?P<thread>[\w.@+-]+)/(?P<pk>[\w.@+-]+)/$", ChatDelete.as_view()),
    re_path(r"^threadlist/(?P<user>[\w.@+-]+)/$", ThreadListView.as_view()),
    re_path(r"^threaddetail/(?P<pk>[\w.@+-]+)/$", ThreadDetailView.as_view()),
     re_path(r"^chatimg/$", Chatimgupload.as_view()),
]
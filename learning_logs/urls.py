"""定义learning_logs的URL模式"""

from django.conf.urls import url
from . import views

urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),  # ^$ 查找开头和末尾之间没有任何东西的url，如：http://localhost:8000/
    url(r'^topics/$', views.topics, name='topics'),
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),  # 正则表达：任何匹配到的数字都存储到topic_id中
    url(r'^new_topic/$', views.new_topic, name='new_topic'),  # 用于添加新主题的网页
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),  # 用于添加新条目的页面
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]

app_name = 'learning_logs'
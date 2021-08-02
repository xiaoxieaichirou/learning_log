"""应用程序users定义URL模式"""

from django.conf.urls import url
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name='users/login.html'), name='login'),  # 登录页面
    url(r'^logout/$', views.logout_view, name='logout'),  # 注销页面
    url(r'^register/$', views.register, name='register'),  # 注册页面
    ]

app_name = 'users'
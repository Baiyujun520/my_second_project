from django.conf.urls import url
from user.views import RegisterView, ActiveView, LoginView, LogoutView, UserInfoView, AddressView

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),  # 注册
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 激活
    url(r'^login$', LoginView.as_view(), name='login'),  # 登录
    url(r'^logout$', LogoutView.as_view(), name='logout'),  # 退出
    url(r'^$', UserInfoView.as_view(), name='user'),  # 用户中心-用户信息
    url(r'^address$', AddressView.as_view(), name='address'),  # 用户中心-用户地址
]
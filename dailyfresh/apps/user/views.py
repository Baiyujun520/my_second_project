from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.core.urlresolvers import reverse
from celery_tasks.tasks import send_register_active_email
from user.models import User
import re

# Create your views here.


class RegisterView(View):
    '''注册类视图'''
    def get(self, request):
        # 进入注册页面
        return render(request, 'register.html')

    def post(self, request):
        # 获取用户输入的信息
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        allow = request.POST.get('allow')
        email = request.POST.get('email')

        # 数据校验，完整性校验
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '输入的数据不完整'})

        # 判断邮箱是否复合规则
        if not re.match('^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱不正确'})

        # 判断是否勾选了用户协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请勾选用户协议'})

        # 判断用户是否已经存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': '用户已经存在'})

        # 业务逻辑处理
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 发送邮件前需要对发送邮件中的链接加密
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode()

        send_register_active_email(email, username, token)

        return redirect(reverse('goods:index'))




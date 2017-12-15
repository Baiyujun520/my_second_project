from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.core.urlresolvers import reverse
from utils.mixin import LoginRequiredMixin
from celery_tasks.tasks import send_register_active_email
from itsdangerous import SignatureExpired
from user.models import User, Address
from goods.models import GoodsSKU
from django_redis import get_redis_connection
import re

# Create your views here.


class RegisterView(View):
    """注册类视图"""
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

        send_register_active_email.delay(email, username, token)

        return redirect(reverse('goods:index'))


class ActiveView(View):
    '''用户激活视图'''
    def get(self, request, token):
        # 将发来的token信息解码
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取要激活的id
            user_id = info['confirm']

            # 根据获取到的用户id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 激活后返回到登录页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            return HttpResponse('连接已失效')


class LoginView(View):
    """登录"""
    def get(self, request):
        """显示登录页面"""
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        # 获取登录时输入的信息
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 数据校验
        # 首先验证数据是否完整
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '您输入的信息不完整'})

        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名和密码正确
            if user.is_active:
                # 用户已经激活
                login(request, user)

                # 获取登录跳转的页面
                next_url = request.GET.get('next', reverse('goods:index'))

                # 登录成功返回首页
                response = redirect(next_url)

                # 获取是否记住用户名，若选择记住，则设置用户的cookie信息
                remember = request.POST.get('remember')
                if remember == 'on':
                    # 设置cookie信息
                    response.set_cookie('username', username)
                else:
                    response.delete_cookie('username')
                return response
            else:
                # 用户账户未激活
                return render(request, 'login.html', {'errmsg': '用户账户未激活'})
        else:
            # 用户和密码不存在
            return render(request, 'login.html', {'errmsg': '用户名或密码不正确'})


class LogoutView(View):
    '''退出'''
    def get(self, request):
        logout(request)

        # 退出重定向到首页
        return redirect(reverse('goods:index'))


class UserInfoView(LoginRequiredMixin, View):
    """用户中心-用户信息"""
    def get(self, request):
        # 显示个人信息
        user = request.user
        address = Address.objects.get_default_address(user=user)
        # 获取用户浏览商品记录
        # 首先跟redis数据库建立连接
        # conn = get_redis_connection('default')
        #
        # # 获取用户的历史浏览记录
        # list_key = 'history_%d' % user.id
        # # 获取到redis中的五条历史记录
        # sku_ids = conn.lrange(list_key, 0, 4)
        # # 获取数据库中对应商品编号的商品
        # goods_li = []
        # for id in sku_ids:
        #     goods = GoodsSKU.objects.get(id=id)
        #     goods_li.append(goods)

        # 构造上下文
        context = {'page': 'user', 'user': user, 'address': address}

        return render(request, "user_center_info.html", context=context)


class AddressView(LoginRequiredMixin, View):
    """用户中心-地址信息"""
    def get(self, request):
        # 显示用户的默认地址
        user = request.user
        address = Address.objects.get_default_address(user=user)

        # 构造上下文
        context = {'page': 'address', 'address': address}
        return render(request, 'user_center_site.html', context)

    def post(self, request):
        """设置地址"""

        # 获取请求传来的参数
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 验证数据的完整性
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})

        # 手机号码验证
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg', '手机号码不正确'})

        # 业务处理
        # 如果用户没有默认的收货地址， 则将添加的值设为默认值，否则不做处理

        # 获取登录对象
        user = request.user

        address = Address.objects.get_default_address(user=user)

        if address:
            is_default = False
        else:
            is_default = True

        # 将地址添加到数据库中
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        return redirect(reverse('user:address'))

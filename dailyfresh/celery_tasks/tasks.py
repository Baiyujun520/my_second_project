from django.core.mail import send_mail
from celery import Celery
from django.conf import settings
import time

# 初始化django项目所依赖的环境
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
django.setup()

# 创建一个celery类
app = Celery('celery_tasks.tasks', broker='redis://192.168.56.137:6379/10')


# 创建发送激活邮件的函数
@app.task
def send_register_active_email(to_email, username, token):
    # 发送激活文件
    subject = '天天生鲜欢迎您注册'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    msg = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/>' \
          '<a href="http://127.0.0.1:8000/user/active/%s">' \
          'http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
    send_mail(subject, message, sender, receiver, html_message=msg)
    time.sleep(5)
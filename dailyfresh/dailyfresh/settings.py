"""
Django settings for dailyfresh project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&7^s_d69k^xrqvemo)3@qstk9te0hz1t+9*_a%%%y6s2figxja'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',  # 富文本编辑器
    'user',  # 用户模块
    'goods',  # 商品模块
    'order',  # 订单模块
    'cart'  # 购物车模块
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'dailyfresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dailyfresh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dailyFresh',
        'HOST': '192.168.56.139',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'mysql',
    }
}

# 使用Django的认证系统的模型类
AUTH_USER_MODEL = 'user.User'
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 富文本编辑器配置
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}


# 邮件发送配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = 'baiyujun010@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'baiyujun520940'
# 收件人看到的发件人
EMAIL_FROM = '天天生鲜<baiyujun010@163.com>'

# 设置登录url地址
LOGIN_URL = '/user/login'

# 七牛云秘钥
QINIU_ACCESS_KEY = 'V_xlJjJOVoTYzXpuY0dKH1s1SF2m5ITXzIqcxwib'
#
QINIU_SECRET_KEY = 'HuNmaIzEabXHBV97VO6Gcmo9ZuQLFW93_yKLxh0a'
QINIU_BUCKET_NAME = 'dailyfresh'
QINIU_BUCKET_DOMAIN = 'p0zgd3uy3.bkt.clouddn.com/'
QINIU_SECURE_URL = False      # 使用http

DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuMediaStorage'

# STATIC_URL = QINIU_BUCKET_DOMAIN + '/static/'

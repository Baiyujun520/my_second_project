from django.core.files.storage import Storage
from qiniu import Auth, put_data
from django.conf import settings


class QINIUStorage(Storage):
    '''fast dfs 文件存储类'''
    def __init__(self):
        '''初始nginx的ip的ip地址端口号,初始化客户端的路径'''
        self.q = Auth(access_key=settings.QINIU_ACCESS_KEY, secret_key=settings.QINIU_SECRET_KEY)
        # 生成上传Token，可以指定时间等
        self.token = self.q.upload_token(settings.QINIU_BUCKET_NAME)
        self.base_url = settings.QINIU_BUCKET_DOMAIN

    def _open(self, name, mode='rb'):
        '''打开文件时使用'''
        pass

    def _save(self, name,  content):
        '''保存文件时使用'''
        # name 是你选择上传的文件的名称
        # content 就是包含你上传文件内容的文件对象File
        ret, info = put_data(self.token, None, content.read())

        # dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }

        if info.status_code != 200:
            raise Exception("七牛上传文件失败")


        return True

    def exists(self, name):
        '''django判断文件是否存在，若存在返回True 若不存在返回False'''
        return False

    def url(self, name):
        # 返回已经上传图片在fdfs上的编码
        return self.base_url + name




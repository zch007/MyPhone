"""
Django线上配置文件
"""

# 项目密钥
SECRET_KEY = 'django-insecure-jk-11od9jlzddt60gitzsbp8q^ofv-j74f9@gz*82a_t-y35@$'

# 调试模式（只适用于本地测试）
DEBUG = False

# 允许访问的主机
ALLOWED_HOSTS = ['*']

# 线上数据库（暂无）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_phone',
        'HOST': '',
        'PORT': None,
        'USER': '',
        'PASSWORD': '',
    }
}

"""
Django核心配置文件
"""

import os
import sys

# 项目base目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 修改默认的子应用的目录
sys.path.insert(0, os.path.join(BASE_DIR, 'modules'))

# 静态文件目录
STATIC_URL = '/static/'

# 资源文件目录
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# 全局路由
ROOT_URLCONF = 'my_phone.config.urls'

# WSGI配置
WSGI_APPLICATION = 'my_phone.config.wsgi.application'

# App挂载
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',  # 解决csrf跨域模块
    'xadmin',  # xadmin主体模块
    'crispy_forms',  # xadmin渲染表格模块
    'reversion',  # 为xadmin中注册模型提供版本控制，方便回滚
    'supervisor',
    'index',
    'users',
    'shop',
    'cart',
]

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 解决csrf跨域
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 模版文件
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

# 密码校验
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/my_phone.log"),
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}

# 语言
LANGUAGE_CODE = 'zh-hans'

# 时区
TIME_ZONE = 'Asia/Shanghai'

# Django国际化支持（用于动态翻译）
USE_I18N = True

# 格式化系统开关
USE_L10N = True

# 数据库存储使用时间，True时间会被存为UTC的时间
USE_TZ = False

# corsheaders允许跨域请求
CORS_ORIGIN_ALLOW_ALL = True

# 指定默认的用户模型
AUTH_USER_MODEL = "users.UserInfo"

"""
Django Rest Framework 配置文件
"""

import datetime

# DRF的全局配置
REST_FRAMEWORK = {
    # DRF配置的全局异常处理的方法
    'EXCEPTION_HANDLER': 'my_phone.config.exceptions.exception_handler',
    # 添加认证方式
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# JWT配置
JWT_AUTH = {
    # token有效期时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3000000),
    # 自定义jwt返回值
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'users.utils.jwt_response_payload_handler',
}

# 指定多条件登陆的类
AUTHENTICATION_BACKENDS = [
    "users.utils.UserAuthBackend",
]

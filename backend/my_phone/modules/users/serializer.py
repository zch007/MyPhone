import re
import random

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.settings import api_settings

from users.models import UserInfo
from users.utils import get_user_by_account


class UserSerializer(ModelSerializer):
    """
    1. 登陆注册的序列化器
    2. 用于校验注册信息
    """
    token = serializers.CharField(max_length=1024, read_only=True, help_text="用户token")
    code = serializers.CharField(write_only=True, help_text="手机验证码")

    class Meta:
        model = UserInfo
        fields = ("phone", "password", "id", "username", "token", "code")

        extra_kwargs = {
            "phone": {
                "write_only": True,
            },
            "password": {
                "write_only": True,
            },
            "username": {
                "read_only": True,
            },
            "id": {
                "read_only": True,
            },
        }

    def validate(self, attrs):
        """
        通过全局钩子来完成注册用户数据的校验
        """
        phone = attrs.get("phone")
        password = attrs.get("password")
        sms_code = attrs.get("code")

        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise serializers.ValidationError("手机号格式错误")

        # 验证手机号是否被注册
        try:
            user = get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user = None

        if user:
            raise serializers.ValidationError("当前手机号已经被注册")

        # 检验密码的格式
        if len(password) < 6 or len(password) > 12:
            raise serializers.ValidationError("密码长度错误")

        # 校验验证码是否一致
        redis_connection = get_redis_connection("sms_code")
        mobile_code = redis_connection.get("mobile_{}".format(phone))
        if mobile_code.decode() != sms_code:
            raise serializers.ValidationError("验证码不一致")

        # 验证通过后将redis的验证码的删除
        redis_connection.delete("sms_{}".format(phone))
        redis_connection.delete("mobile_{}".format(phone))

        return attrs

    def create(self, validated_data):
        """
        用于注册用户
        """
        phone = validated_data.get("phone")

        # 获取密码  对密码进行加密
        password = validated_data.get("password")
        hash_password = make_password(password)

        # 处理用户名的默认值
        username = "MyPhone_{:06d}".format(random.randint(0, 999999))

        # 保存数据
        user = UserInfo.objects.create(
            phone=phone,
            username=username,
            password=hash_password
        )

        # 为注册的用户手动生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user

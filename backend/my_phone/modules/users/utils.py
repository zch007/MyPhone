import requests
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import UserInfo


def jwt_response_payload_handler(token, user=None, request=None):
    """
    根据用户和密码获取token
    """
    return {
        "token": token,
        "user": user.username,
        "user_id": user.id
    }


def get_user_by_account(account):
    """
    根据条件获取用户
    """
    try:
        user = UserInfo.objects.filter(Q(username=account) | Q(email=account) | Q(phone=account)).first()
    except UserInfo.DoesNotExist:
        return None

    return user


class UserAuthBackend(ModelBackend):
    """
    自定义多方式登陆
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """根据账号来获取用户登陆方式   手机号  邮箱  用户名"""
        user = get_user_by_account(username)

        if user and user.check_password(password) and user.is_authenticated:
            return user

        return None


class Message(object):
    """
    发送短信验证码
    """

    def __init__(self, api_key):
        self.api_key = api_key  # 账号的唯一标识
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_message(self, phone, code):
        params = {
            "apikey": self.api_key,
            "mobile": phone,
            "text": "【MyPhone】您的验证码是{}。如非本人操作，请忽略本短信".format(code)
        }

        requests.post(self.single_send_url, data=params)
        print("短信发送 OK")

import random
import re

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status
from rest_framework_jwt.settings import api_settings
from django_redis import get_redis_connection

from my_phone.utils.geetest import GeetestLib
from my_phone.config import parameter
from users.models import UserInfo
from users.serializer import UserSerializer
from users.utils import get_user_by_account, Message


class CaptchaAPIView(APIView):
    """
    获取滑块验证码
    """
    pc_geetest_id = "1ea3ed8b35299a931b6a3883ec4a05be"
    pc_geetest_key = "9a13879615c1ae2500e356417cd5bcf9"
    user_id = 0
    status = False

    def get(self, request, *args, **kwargs):
        """pc端获取验证码"""
        username = request.query_params.get("username")
        user = get_user_by_account(username)
        self.user_id = user.id

        gt = GeetestLib(self.pc_geetest_id, self.pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        response_str = gt.get_response_str()

        return Response(response_str)

    def post(self, request, *args, **kwargs):
        """pc端基于前后端分离校验验证码"""
        gt = GeetestLib(self.pc_geetest_id, self.pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')

        if self.user_id:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}

        return Response(result)


class SendMessageAPIView(APIView):
    """
    发送短信业务
    """

    def get(self, request, *args, **kwargs):
        """
        获取验证码   为手机号生成验证码并发送
        """
        phone = request.query_params.get("phone")

        if not phone:
            return Response({"message": "尚未输入手机号"}, status=http_status.HTTP_400_BAD_REQUEST)

        print("手机号: {}".format(phone))

        redis_connection = get_redis_connection("sms_code")

        # TODO 1.判断用户60s内是否发送过验证码
        mobile_code = redis_connection.get("sms_{}".format(phone))

        if mobile_code:
            return Response({"message": "您已经在60s内发送过短信了，请稍等~"}, status=http_status.HTTP_400_BAD_REQUEST)

        # TODO 2.生成随机验证码
        code = "{:06d}".format(random.randint(0, 999999))
        print("验证码: {}".format(code))

        # TODO 3.将验证码保存在redis中
        redis_connection.setex("sms_{}".format(phone), parameter.SMS_EXPIRE_TIME, code)  # 验证码间隔时间
        redis_connection.setex("mobile_{}".format(phone), parameter.CODE_EXPIRE_TIME, code)  # 验证码有效期

        # TODO 4.完成短信的发送
        try:
            message = Message(parameter.API_KEY)
            message.send_message(phone, code)
        except:
            return Response({"message": "验证码发送失败"}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        # TODO 5.将发送的结果响应回去
        return Response({"message": "短信发送成功"}, status=http_status.HTTP_200_OK)


class RegisterAPIView(CreateAPIView):
    """
    用户注册逻辑
    """
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializer


class MessageLoginAPIView(APIView):
    """
    短信登录逻辑
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        code = request.data.get("code")

        try:
            user = UserInfo.objects.get(phone=phone)

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            user.token = jwt_encode_handler(payload)

            redis_connection = get_redis_connection("sms_code")
            mobile_code = redis_connection.get("mobile_{}".format(phone))

            if mobile_code.decode() == code:
                # 删除redis中的缓存
                redis_connection.delete("sms_{}".format(phone))
                redis_connection.delete("mobile_{}".format(phone))

                return Response({
                    "token": user.token,
                    "phone": phone,
                })
        except:
            return Response({"message": "手机号未注册"}, status=http_status.HTTP_400_BAD_REQUEST)

        return Response({"message": "验证码错误"}, status=http_status.HTTP_400_BAD_REQUEST)


class RegisterMobileCheckAPIView(APIView):
    """
    注册时输入手机号后验证
    """

    def get(self, request):
        phone = request.query_params.get("phone")

        if not re.match(r'^1[3-9]\d{9}$', phone):
            return Response({"message": "手机号格式不正确"}, status=http_status.HTTP_400_BAD_REQUEST)

        user = get_user_by_account(phone)

        if user:
            return Response({"message": "手机号已经被注册"}, status=http_status.HTTP_400_BAD_REQUEST)

        return Response({"message": "OK"})


class LoginMobileCheckAPIView(APIView):
    """
    登陆时输入手机号后验证
    """

    def get(self, request, *args, **kwargs):
        phone = request.query_params.get("phone")

        if not re.match(r'^1[3-9]\d{9}$', phone):
            return Response({"message": "手机号格式不正确"}, status=http_status.HTTP_400_BAD_REQUEST)

        user = get_user_by_account(phone)

        if not user:
            return Response({"message": "手机号不存在"}, status=http_status.HTTP_400_BAD_REQUEST)

        return Response({"message": "OK"})

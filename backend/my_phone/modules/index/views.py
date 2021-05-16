from django_redis import get_redis_connection
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from my_phone.config import parameter
from index.models import Banner, Nav
from index.serializers import BannerSerializer, NavSerializer


class BannerAPIView(ListAPIView):
    """
    获取轮播图
    """
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by("-orders")[:parameter.BANNER_LENGTH]
    serializer_class = BannerSerializer


class NavTopAPIView(ListAPIView):
    """
    获取顶部导航
    """
    queryset = Nav.objects.filter(is_show=True, is_delete=False, position=1).order_by("orders")[:parameter.NAV_TOP_LENGTH]
    serializer_class = NavSerializer


class NavBottomAPIView(ListAPIView):
    """
    获取底部导航
    """
    queryset = Nav.objects.filter(is_show=True, is_delete=False, position=2).order_by("orders")[:parameter.NAV_BOTTOM_LENGTH]
    serializer_class = NavSerializer


class CartAPIView(APIView):
    """
    购物车数量显示
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        course_len = redis_connection.hlen("cart_{}".format(user_id))
        return Response({"cart_length": course_len})


class UserAPIView(APIView):
    """
    用户信息显示
    """
    permission_class = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        username = user.username
        email = user.email
        phone = user.phone
        return Response(
            {
                "username": username,
                "email": email,
                "phone": phone
            }
        )

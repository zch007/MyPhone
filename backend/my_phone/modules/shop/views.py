from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from shop.models import Category, Phone, Evaluation
from shop.pagination import PhonePagination
from shop.serializers import CategorySerializer, PhoneSerializer, PhoneDetailSerializer, EvaluationSerializer


class CategoryAPIView(ListAPIView):
    """
    手机分类信息
    """
    queryset = Category.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CategorySerializer


class PhoneAPIView(ListAPIView):
    """
    商品列表信息
    """
    queryset = Phone.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = PhoneSerializer

    # 根据不同的分类id来展示查询对应的课程
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # 指定查询的字段
    filter_fields = ["category"]
    # 指定课程可以排序的条件
    ordering_fields = ["id", "user_num", "price"]
    # 指定分页的类
    pagination_class = PhonePagination


class PhoneDetailAPIView(RetrieveAPIView):
    """
    手机详情信息
    """
    queryset = Phone.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = PhoneDetailSerializer


class EvaluationAPIView(ListAPIView):
    """
    评测列表信息
    """
    queryset = Evaluation.objects.filter(is_show=True, is_delete=False).order_by("id")
    serializer_class = EvaluationSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["phone"]

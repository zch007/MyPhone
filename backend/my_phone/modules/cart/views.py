from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from django_redis import get_redis_connection

from shop.models import Phone
from my_phone.config import parameter


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def add_cart(self, request, *args, **kwargs):
        """将用户在前端提交的信息保存至购物车"""
        phone_id = request.data.get("phone_id")
        user_id = request.user.id

        try:
            Phone.objects.get(is_show=True, is_delete=False, pk=phone_id)
        except Phone.DoesNotExist:
            return Response({"message": "参数有误，商品不存在"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            redis_connection = get_redis_connection("cart")
            pipeline = redis_connection.pipeline()
            pipeline.hset("cart_{}".format(user_id), phone_id, "")
            pipeline.sadd("selected_{}".format(user_id), phone_id)
            pipeline.execute()
            # 获取购物车中商品的总数据量
            cart_length = redis_connection.hlen("cart_{}".format(user_id))
        except:
            return Response({"message": "参数有误，购物车添加失败"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({"message": "购物车添加成功", "cart_length": cart_length})

    def list_cart(self, request, *args, **kwargs):
        """购物车展示"""
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        cart_list_bytes = redis_connection.hgetall("cart_{}".format(user_id))
        selected_list_bytes = redis_connection.smembers("selected_{}".format(user_id))

        data = []
        for phone_id_byte, _ in cart_list_bytes.items():
            phone_id = int(phone_id_byte)

            try:
                phone = Phone.objects.get(is_show=True, pk=phone_id, is_delete=False)
            except Phone.DoesNotExist:
                continue

            data.append({
                "selected": True if phone_id_byte in selected_list_bytes else False,
                "cover": parameter.IMG_SRC + phone.cover.url,
                "name": phone.name,
                "price": phone.real_price,
                "id": phone.id,
            })

        return Response(data)

    def mod_select(self, request, *args, **kwargs):
        """修改选中状态"""
        phone_id = request.data.get("phone_id")
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        is_check = redis_connection.sismember("selected_{}".format(user_id), phone_id)

        if is_check:
            redis_connection.srem("selected_{}".format(user_id), phone_id)
        else:
            redis_connection.sadd("selected_{}".format(user_id), phone_id)

        return Response("ok")

    def del_course(self, request, *args, **kwargs):
        """删除商品"""
        phone_id = request.data.get("phone_id")
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        redis_connection.hdel("cart_{}".format(user_id), phone_id)
        return Response("ok")


class OrderShowAPIView(ViewSet):
    """
    购物车结算页面
    """
    permission_classes = [IsAuthenticated]

    def get_select_course(self, request):
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        cart_list = redis_connection.hgetall("cart_{}".format(user_id))
        select_list = redis_connection.smembers("selected_{}".format(user_id))
        total_price = 0
        data = []
        print(cart_list, "\n", select_list)

        for phone_id_byte, _ in cart_list.items():
            phone_id = int(phone_id_byte)

            if phone_id_byte in select_list:
                try:
                    phone = Phone.objects.get(is_delete=False, is_show=True, pk=phone_id)
                except Phone.DoesNotExist:
                    continue

                price = phone.real_price

                data.append({
                    "cover": parameter.IMG_SRC + phone.cover.url,
                    "name": phone.name,
                    "price": price,
                    "id": phone.id,
                })

                total_price += float(price)

        return Response({"phone_list": data, "total_price": total_price, "message": "获取成功"})

from datetime import datetime
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django_redis import get_redis_connection
from course.models import Course, CourseExpire
from order.models import Order, OrderDetail


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "order_number", "pay_type")
        extra_kwargs = {
            "id": {"read_only": True},
            "order_number": {"read_only": True},
            "pay_type": {"write_only": True},
        }

    # 对数据进行校验
    def validate(self, attrs):
        pay_type = attrs.get("pay_type")
        try:
            Order.pay_choices[pay_type]
        except Order.DoesNotExist:
            raise serializers.ValidationError("您当前选择的支付方式不允许~")
        return attrs

    # 创建订单详情
    def create(self, validated_data):
        # TODO 1. 需要获取当前订单所需的课程数据
        redis_connection = get_redis_connection("cart")
        # 获取到当前登录的用户对象
        user_id = self.context['request'].user.id
        user_id = 1
        incr = redis_connection.incr("number")
        # TODO 2. 生成唯一的订单号  时间戳  用户ID  随机字符串
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + "%06d" % user_id + "%06d" % incr
        # TODO 3. 订单的生成
        order = Order.objects.create(
            order_title="百知教育在线商城订单",
            total_price=0,
            real_price=0,
            order_number=order_number,
            order_status=0,
            pay_type=validated_data.get("pay_type"),
            credit=0,
            coupon=0,
            order_desc="你不会后悔的选择！！！",
            user_id=user_id,
        )
        cart_list = redis_connection.hgetall("cart_%s" % user_id)
        select_list = redis_connection.smembers("selected_%s" % user_id)
        # TODO 4. 生成订单详情
        """
        1. 获取购物车中所以后被勾选的商品
        2. 判断商品是否在已勾选的列表中
        3. 判断课程的状态是否正常  不正常直接抛出异常
        4. 判断商品的有效期  根据有效期计算商品优惠后的价格
        5. 生成订单详情。
        6. 计算订单的总价  原价
        """
        for course_id_byte, expire_id_byte in cart_list.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            # 判断商品是否被勾选
            if course_id_byte in select_list:
                # 获取课程的所有信息
                try:
                    course = Course.objects.get(is_delete=False, is_show=True, pk=course_id)
                    expire_list = course.expire_text
                    expire_price = 0
                    for item in expire_list:
                        if item["id"] == expire_id:
                            expire_price = item["price"]
                except Course.DoesNotExist:
                    raise serializers.ValidationError("对不起，您所购买的商品不存在")
                # 如果课程的有效期id大于0，则需要重新计算商品的价格，id不大于0则是永久有效
                origin_price = expire_price
                expire_text = "永久有效"
                if expire_id > 0:
                    course_expire = CourseExpire.objects.get(pk=expire_id)
                    # 获取有效期对应的原价
                    origin_price = course_expire.price
                    expire_text = course_expire.expire_text
                final_price = expire_price
                try:
                    OrderDetail.objects.create(
                        order=order,
                        course=course,
                        expire=expire_id,
                        price=origin_price,
                        real_price=final_price,
                        discount_name=course.discount_name
                    )
                except:
                    raise serializers.ValidationError("订单生成失败")
                # 计算订单的总价  原价
                order.total_price += float(origin_price)
                order.real_price += float(final_price)
            order.save()
            # TODO 5. 如果商品已经成功生成了订单  需要 将该商品从购物车中移除
        return order

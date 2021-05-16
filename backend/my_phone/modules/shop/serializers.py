from rest_framework.serializers import ModelSerializer

from shop.models import Category, Phone, Evaluation


class CategorySerializer(ModelSerializer):
    """
    手机分类序列化器
    """

    class Meta:
        model = Category
        fields = ["id", "name"]


class EvaluationSerializer(ModelSerializer):
    """
    评测信息序列化器
    """

    class Meta:
        model = Evaluation
        fields = ["id", "title", "summary", "pub_date", "is_site", "author", "content"]


class PhoneSerializer(ModelSerializer):
    """
    手机列表序列化器
    """
    evaluation = EvaluationSerializer(many=True)

    class Meta:
        model = Phone
        fields = ["id", "name", "cover", "brief",  "user_num", "price", "evaluation", "discount_name", "real_price"]


class PhoneDetailSerializer(ModelSerializer):
    """
    手机详情序列化器
    """
    evaluation = EvaluationSerializer(many=True)

    class Meta:
        model = Phone
        fields = ["id", "name", "cover", "brief", "video", "content", "user_num", "price", "evaluation",
                  "discount_name", "active_time", "real_price"]

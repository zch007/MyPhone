from rest_framework.serializers import ModelSerializer

from index.models import Banner, Nav


class BannerSerializer(ModelSerializer):
    """
    轮播图
    """

    class Meta:
        model = Banner
        fields = ["title", "img", "link"]


class NavSerializer(ModelSerializer):
    """
    导航栏
    """

    class Meta:
        model = Nav
        fields = ["title", "link", "is_site"]

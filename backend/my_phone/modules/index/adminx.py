import xadmin
from index.models import Banner, Nav


class BannerInfo(object):
    """
    轮播图
    """
    list_display = ["title", "orders", "is_show", "create_time", "update_time"]


xadmin.site.register(Banner, BannerInfo)


class NavInfo(object):
    """
    导航栏
    """
    list_display = ["title", "orders", "is_show", "create_time", "update_time"]


xadmin.site.register(Nav, NavInfo)

import xadmin

from shop import models


class CategoryInfo(object):
    """
    分类信息
    """
    list_display = ["name", "orders", "is_show", "create_time", "update_time"]


xadmin.site.register(models.Category, CategoryInfo)


class PhoneInfo(object):
    """
    手机信息
    """
    list_display = ["name", "orders", "is_show", "create_time", "update_time"]


xadmin.site.register(models.Phone, PhoneInfo)


class EvaluationInfo(object):
    """
    评测信息
    """
    list_display = ["title", "phone", "orders", "is_show", "create_time", "update_time"]


xadmin.site.register(models.Evaluation, EvaluationInfo)


class DiscountTypeInfo(object):
    """
    优惠类型
    """
    list_display = ["name", "orders", "is_show", "create_time", "update_time"]


xadmin.site.register(models.DiscountType, DiscountTypeInfo)


class DiscountInfo(object):
    """
    优惠策略
    """
    list_display = ["discount_type", "orders", "is_show", "create_time", "update_time"]


xadmin.site.register(models.Discount, DiscountInfo)


class ActivityInfo(object):
    """
    优惠活动
    """
    list_display = ["name", "orders", "is_show", "create_time", "update_time"]


xadmin.site.register(models.Activity, ActivityInfo)


class DiscountRelationInfo(object):
    """
    商品与优惠策略的关系
    """
    list_display = ["phone", "active", "discount", "orders", "is_show", "create_time", "update_time"]


xadmin.site.register(models.DiscountRelation, DiscountRelationInfo)

from datetime import datetime

from django.db import models
from my_phone.config.base_model import BaseModel


class Category(BaseModel):
    """
    手机分类
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")

    class Meta:
        db_table = "t_category"
        verbose_name = "手机分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.name)


class Phone(BaseModel):
    """
    手机信息
    """
    status_choices = (
        (0, "在售"),
        (1, "停产"),
        (2, "预售"),
    )
    name = models.CharField(max_length=128, verbose_name="手机名称")
    cover = models.ImageField(upload_to="phone", max_length=255, verbose_name="封面图片", blank=True, null=True,
                              help_text="请上传978*550的图片")
    video = models.FileField(upload_to="video", null=True, blank=True, verbose_name="视频")
    brief = models.CharField(max_length=128, verbose_name="简介", null=True, blank=True)
    content = models.TextField(verbose_name="内容", null=True, blank=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="出售状态")
    user_num = models.IntegerField(verbose_name="使用人数", default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="原价", default=0)
    category = models.ForeignKey("Category", related_name="phone", on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name="手机分类")

    class Meta:
        db_table = "t_phone"
        verbose_name = "手机信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.name)

    def relation_list(self):
        """获取商品优惠关系列表"""
        relation_list = self.relation.filter(is_show=True, is_delete=False,
                                             active__start_time__lte=datetime.now(),
                                             active__end_time__gte=datetime.now()).order_by("orders")
        return relation_list

    @property
    def discount_name(self):
        """获取当前所参与的优惠活动名称"""
        name = ""
        relation_list = self.relation_list()

        # 当前课程参与了优惠活动才返回活动名称
        if len(relation_list) > 0:
            relation = relation_list[0]
            name = relation.active.name

        return name

    @property
    def real_price(self):
        """计算商品的真实价格"""
        price = self.price
        relation_list = self.relation_list()

        # 如果商品参与了活动，则根据所参与的活动计算价格
        if len(relation_list) > 0:
            relation = relation_list[0]
            condition = relation.discount.condition
            formula = relation.discount.formula
            self.price = float(self.price)

            # 判断课程价格的原价是否满足优惠条件的门槛
            if self.price >= condition:
                # 判断当前课程满足哪一种优惠条件
                if formula == "":  # 限时免费
                    price = 0
                elif formula[0] == "*":  # 限时折扣
                    price = self.price * float(formula[1:])
                elif formula[0] == "-":  # 限时减免
                    price = self.price - float(formula[1:])
                elif formula[0] == "满":  # 满减 如500-80  400-40 300-20 200-10
                    split = formula.split("\r\n")
                    formula_list = []

                    for item in split:
                        formula_item = item[1:]
                        condition_price, condition_formula = formula_item.split("-")
                        if self.price >= float(condition_price):
                            formula_list.append(float(condition_formula))

                    if len(formula_list) > 0:
                        # 课程原价减去当前满足条件中最高的优惠价格
                        price = self.price - max(formula_list)

        return "{:.2f}".format(price)

    @property
    def active_time(self):
        """返回活动剩余时间"""
        time = 0
        relation_list = self.relation_list()

        if len(relation_list) > 0:
            relation = relation_list[0]
            now_time = datetime.now().timestamp()
            end_time = relation.active.end_time.timestamp()
            time = end_time - now_time

        return int(time)


class Evaluation(BaseModel):
    """
    评测信息
    """
    phone = models.ForeignKey("Phone", related_name="evaluation", on_delete=models.CASCADE, verbose_name="手机名称")
    title = models.CharField(max_length=128, verbose_name="评测标题")
    summary = models.TextField(verbose_name="摘要", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    is_site = models.BooleanField(default=False, verbose_name="是否是站外评测")
    author = models.CharField(max_length=20, verbose_name="评测来源")
    content = models.TextField(max_length=2048, verbose_name="评测内容", blank=True, null=True,
                               help_text="若是用户评测，则记录评测内容，若是站外评测，则记录链接")
    is_show_list = models.BooleanField(verbose_name="是否展示到分类页面", default=False)

    class Meta:
        db_table = "t_evaluation"
        verbose_name = "评测"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "【{}】{}:{}".format(self.phone.category, self.phone, self.title)


class DiscountType(BaseModel):
    """
    优惠类型
    """
    name = models.CharField(max_length=32, verbose_name="优惠类型名称")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "t_discount_type"
        verbose_name = "优惠类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.name)


class Discount(BaseModel):
    """
    优惠策略
    """
    discount_type = models.ForeignKey("DiscountType", on_delete=models.CASCADE, related_name="discount",
                                      verbose_name="优惠类型")
    condition = models.IntegerField(blank=True, null=True, default=0, verbose_name="满足优惠的价格条件",
                                    help_text="设置参与优惠的价格门槛，表示商品必须在xx价格以上的时候才参与优惠活动，<br>如果不填，则不设置门槛")
    formula = models.TextField(verbose_name="优惠公式", blank=True, help_text="""
    不填表示免费；<br>
    *号开头表示折扣价，例如*0.82表示八二折；<br>
    -号开头则表示减免，例如-20表示原价-20；<br>
    如果需要表示满减,则需要使用 原价-优惠价格,例如表示价格大于100,优惠10;大于200,优惠20,格式如下:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满100-10<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满200-25<br>
    """)

    class Meta:
        db_table = "t_discount"
        verbose_name = "优惠策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "优惠名称:{},优惠条件:{},优惠公式:{}".format(self.discount_type.name, self.condition, self.formula)


class Activity(BaseModel):
    """
    优惠活动
    """
    name = models.CharField(max_length=150, verbose_name="活动名称")
    start_time = models.DateTimeField(verbose_name="优惠策略的开始时间")
    end_time = models.DateTimeField(verbose_name="优惠策略的结束时间")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "t_activity"
        verbose_name = "优惠活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DiscountRelation(BaseModel):
    """
    商品与优惠策略关系表
    """
    phone = models.ForeignKey("Phone", on_delete=models.CASCADE, related_name="relation", verbose_name="商品")
    active = models.ForeignKey("Activity", on_delete=models.DO_NOTHING, related_name="relation", verbose_name="优惠活动")
    discount = models.ForeignKey("Discount", on_delete=models.CASCADE, related_name="relation", verbose_name="优惠折扣")

    class Meta:
        db_table = "t_discount_relation"
        verbose_name = "商品与优惠策略关系"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "商品名:{},优惠活动:{},开始时间:{},结束时间:{}".format(
            self.phone.name, self.active.name, self.active.start_time, self.active.end_time
        )

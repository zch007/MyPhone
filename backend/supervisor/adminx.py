"""
xadmin 基本配置
"""

import xadmin
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    site_title = "MyPhone后台管理系统"
    site_footer = "郑成宏 <zzzch007@126.com>"
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)

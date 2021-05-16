import xadmin

from django.conf import settings
from django.urls import path, re_path, include
from django.views.static import serve
from xadmin.plugins import xversion

# 配置version模块用来自动注册需要版本控制的model
xversion.register_models()

urlpatterns = [
    path('supervisor/', xadmin.site.urls),
    path('index/', include('index.urls')),
    path('users/', include('users.urls')),
    path('shop/', include('shop.urls')),
    path('cart/', include('cart.urls')),

    # 静态资源文件路径
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
]

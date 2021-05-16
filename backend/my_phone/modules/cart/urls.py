from django.urls import path

from cart import views

urlpatterns = [
    path("option/", views.CartViewSet.as_view({"post": "add_cart", "get": "list_cart", "put": "mod_select", "delete": "del_course"})),
    path("order/", views.OrderShowAPIView.as_view({"get": "get_select_course"}))
]

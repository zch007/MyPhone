from django.urls import path

from index import views

app_name = "index"

urlpatterns = [
    path('banner/', views.BannerAPIView.as_view()),
    path('nav_top/', views.NavTopAPIView.as_view()),
    path('nav_bottom/', views.NavBottomAPIView.as_view()),
    path('cart_show/', views.CartAPIView.as_view()),
    path('user/', views.UserAPIView.as_view()),
]

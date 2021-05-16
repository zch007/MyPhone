from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from users import views

app_name = "users"

urlpatterns = [
    path("code_login/", obtain_jwt_token),
    path("message_login/", views.MessageLoginAPIView.as_view()),
    path("captcha/", views.CaptchaAPIView.as_view()),
    path("register/", views.RegisterAPIView.as_view()),
    path("register_mobile_check/", views.RegisterMobileCheckAPIView.as_view()),
    path("login_mobile_check/", views.LoginMobileCheckAPIView.as_view()),
    path("send/", views.SendMessageAPIView.as_view()),
]

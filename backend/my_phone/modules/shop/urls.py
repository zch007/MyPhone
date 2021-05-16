from django.urls import path

from shop import views

app_name = "shop"
urlpatterns = [
    path("category/", views.CategoryAPIView.as_view()),
    path("list/", views.PhoneAPIView.as_view()),
    path("detail/<str:pk>/", views.PhoneDetailAPIView.as_view()),
    path("evaluation/", views.EvaluationAPIView.as_view()),
]

from django.urls import path
from .views import SignUpView
from news.views import UserArticleView

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("writer/", UserArticleView.as_view(), name="user"),
]

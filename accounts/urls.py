from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # ✅ 추가: Django가 제공하는 로그인/로그아웃 뷰 사용

urlpatterns = [
    # ✅ 추가: 회원가입은 우리가 직접 만든 signup 뷰가 처리
    path("signup/", views.signup, name="signup"),

    # ✅ 추가: 로그인은 Django 기본 LoginView 사용 (템플릿만 우리가 제공)
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),

    # ✅ 추가: 로그아웃은 Django 기본 LogoutView 사용
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

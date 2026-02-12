from django.contrib import admin
from django.urls import path, include

from expenses import views as expense_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

# ✅ 루트(/)를 대시보드로 설정
    # 로그인 안 되어 있으면 LOGIN_URL로 자동 이동
    path("", expense_views.dashboard, name="home"),

    path("accounts/", include("accounts.urls")),
    path("expenses/", include("expenses.urls")),

    # ✅ 계좌 관리
    path("banking/", include("banking.urls")),

    # 대시보드
    path("dashboard/", expense_views.dashboard, name="dashboard"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
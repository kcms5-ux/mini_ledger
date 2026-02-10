from django.contrib import admin
from django.urls import path, include

from django.conf import settings  # ✅ 추가
from django.conf.urls.static import static  # ✅ 추가

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("expenses/", include("expenses.urls")),
]

# ✅ 추가: 개발(DEBUG=True)일 때만 static 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
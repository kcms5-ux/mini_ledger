from django.contrib import admin
from .models import Expense  # ✅ 추가: 우리가 만든 모델 가져오기

# ✅ 추가: Expense를 admin에서 관리할 수 있게 등록
admin.site.register(Expense)
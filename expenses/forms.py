# 입력값 전달

from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    """
    Expense 모델 기반 폼
    - user는 폼에 포함하지 않음(서버에서 request.user로 강제 지정)
    """

    class Meta:
        model = Expense

        # ✅ 변경: category 추가 + 원하는 순서로 배치
        fields = ["category", "amount", "memo", "spent_at"]

        widgets = {
            "spent_at": forms.DateInput(attrs={"type": "date"}),
        }
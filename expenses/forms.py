# 입력값 전달

from django import forms
from banking.models import Account
from .models import Expense


class ExpenseForm(forms.ModelForm):
    """
    - account 선택지는 현재 로그인 유저의 계좌만
    - tx_type(IN/OUT)을 폼에 노출
    """

    account = forms.ModelChoiceField(
        queryset=Account.objects.none(),
        required=False,
        empty_label="(계좌 선택)",
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields["account"].queryset = Account.objects.filter(user=user, is_active=True).order_by("-id")

    class Meta:
        model = Expense

        # ✅ 변경: tx_type 추가 + 원하는 순서로 배치
        fields = ["account", "tx_type", "category", "amount", "memo", "spent_at"]

        widgets = {
            "spent_at": forms.DateInput(attrs={"type": "date"}),
        }

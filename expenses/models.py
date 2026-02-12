from django.db import models
from django.conf import settings


class Expense(models.Model):
    """
    지금은 모델명이 Expense지만, 실제 역할은 '거래(Transaction)'에 가까움.
    - tx_type: IN(수입) / OUT(지출)
    """

    class TxType(models.TextChoices):
        IN = "IN", "수입"
        OUT = "OUT", "지출"

    class Category(models.TextChoices):
        FOOD = "FOOD", "음식/식비"
        TRANSPORT = "TRANSPORT", "교통"
        SHOPPING = "SHOPPING", "쇼핑"
        LIVING = "LIVING", "생활"
        ETC = "ETC", "기타"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses",
    )

    account = models.ForeignKey(
        "banking.Account",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )

    # ✅ 추가: 수입/지출 타입 (기존 데이터 보호를 위해 기본값은 OUT)
    tx_type = models.CharField(
        max_length=3,
        choices=TxType.choices,
        default=TxType.OUT,
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.FOOD,
    )

    amount = models.PositiveIntegerField()
    memo = models.CharField(max_length=200, blank=True)
    spent_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} | {self.tx_type} | {self.category} | {self.amount} | {self.spent_at}"
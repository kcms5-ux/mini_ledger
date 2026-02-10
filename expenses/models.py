from django.db import models
from django.conf import settings


class Expense(models.Model):
    """
    지출(Expense) 모델
    - category: 카테고리(선택지 고정)
    - amount: 지출 금액(양수)
    - memo: 메모(선택)
    - spent_at: 날짜
    """

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

    # ✅ 추가: 카테고리(드롭다운 선택)
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
        return f"{self.user} | {self.category} | {self.amount} | {self.spent_at}"
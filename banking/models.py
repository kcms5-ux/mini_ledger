from django.db import models
from django.conf import settings


class Account(models.Model):
    """
    ✅ 계좌(Account)
    - user: 계좌 소유자(로그인 유저)
    - name: 계좌 별칭(예: 카카오뱅크 통장, 우리카드)
    - institution: 은행/카드사(예: 카카오뱅크, 우리은행, 현대카드)
    - account_number: 계좌번호/카드번호(옵션) -> 화면에서는 마스킹으로 보여줄 것
    - is_active: 사용 여부(비활성 계좌 숨김 처리 가능)
    - created_at: 생성 시각
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    name = models.CharField(max_length=50)
    institution = models.CharField(max_length=50, blank=True)
    account_number = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def masked_number(self) -> str:
        """
        ✅ 계좌/카드번호 마스킹
        - 너무 길게 저장하지 않아도 되고, 화면 표시용으로만 사용
        """
        n = (self.account_number or "").strip()
        if not n:
            return ""
        if len(n) <= 4:
            return "*" * len(n)
        return "*" * (len(n) - 4) + n[-4:]

    def __str__(self) -> str:
        # admin / shell에서 보기 좋게
        inst = f"{self.institution} " if self.institution else ""
        return f"{inst}{self.name}"
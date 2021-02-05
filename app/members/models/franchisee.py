from django.db import models

from members.models import PayGoUserManager, PayGoUser, AgencyUser


class FranchiseeUserManager(PayGoUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=PayGoUser.TYPE_FRANCHISEE)


class FranchiseeUser(PayGoUser):

    objects = FranchiseeUserManager()

    class Meta:
        proxy = True
        verbose_name = '가맹점주'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        self.type = PayGoUser.TYPE_FRANCHISEE
        super().save(*args, **kwargs)


class Memo(models.Model):
    franchisee_user = models.ForeignKey(FranchiseeUser, related_name='memos',
                                        on_delete=models.PROTECT,
                                        help_text="가맹점주메모")
    sales_slip = models.CharField('매출전표', max_length=100, blank=True, null=True)
    vat_notation = models.CharField('부가세표기', max_length=100, blank=True, null=True)
    payment_notice = models.CharField('결제공지', max_length=100, blank=True, null=True)
    modify_text = models.TextField('변경사항', default='')
    created_date = models.DateTimeField('생성날짜', auto_now_add=True)
    updated_date = models.DateTimeField('업데이트된날짜', auto_now=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = '가맹점주 메모'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'{self.franchisee_user} {self.modify_text} 변경됨'

from datetime import datetime
from django.db import models

from members.models import PayGoUser


class Payment(models.Model):
    ON_REQUEST, APPROVING, OK, CANCEL = 'on_request', 'approving', 'ok', 'cancel'
    REQUEST_STATUS = (
        (ON_REQUEST, 'on_request'),
        (APPROVING, 'approving'),
        (OK, 'ok'),
        (CANCEL, 'cancel'),
    )
    paygouser = models.ForeignKey(PayGoUser, on_delete=models.PROTECT, related_name='payments', help_text='유저')
    # 주문 번호 밑에 def static 만드는거 어떤가?
    order_number = models.CharField('주문번호', max_length=25, default='PAYGO' + datetime.now().strftime('%H%M%S%f'))
    goods_name = models.CharField('상품_이름', max_length=50)
    card_num = models.CharField('카드숫자', max_length=30)
    card_pwd = models.CharField('카드비밀번호_앞자리_두개', max_length=2)
    card_avail_year = models.CharField('카드_유효_연도', max_length=4)
    card_avail_month = models.CharField('카드_유효_월', max_length=2)
    price = models.PositiveIntegerField('가격')
    status = models.CharField('상태', max_length=10, blank=True, null=True, choices=REQUEST_STATUS, default=ON_REQUEST)
    card_quota = models.CharField('할부개월', max_length=2)
    buyer_name = models.CharField('구매자_이름', max_length=20)
    buyer_auth_num = models.CharField('주민등록번호_앞자리', max_length=6)
    buyer_tel = models.CharField('구매자_휴대폰번호', max_length=20)
    buyer_email = models.CharField('구매자_이메일', max_length=50)
    is_canceled = models.BooleanField(default=False)
    payed_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = '결제 내역 정보'
        verbose_name_plural = '%s 목록' % verbose_name
        unique_together = ('paygouser', 'order_number', 'is_canceled')

    def __str__(self):
        return f'유저 : {self.paygouser} | ' \
               f'구매자 정보 : {self.buyer_email if self.buyer_email is not None else self.buyer_tel}'

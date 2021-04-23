from datetime import datetime
from django.db import models

from members.models import PayGoUser


class Payment(models.Model):
    ON_REQUEST, WAIT, APPROVING, BEFORE_CANCEL, PARTIAL_CANCEL, CANCEL = 'on_request', 'wait', 'approving', \
                                                                         'before_cancel', 'partial_cancel', 'cancel'
    REQUEST_STATUS = (
        (ON_REQUEST, '거래요청'),
        (WAIT, '결제대기'),
        (APPROVING, '거래승인'),
        (BEFORE_CANCEL, '매입전취소'),
        (PARTIAL_CANCEL, '부분취소'),
        (CANCEL, '거래취소'),
    )

    paygouser = models.ForeignKey(PayGoUser, on_delete=models.PROTECT, related_name='payments', help_text='유저')
    # 주문 번호 밑에 def static 만드는거 어떤가?
    # 과거 문제가 일단 없던 거임
    # order_number = models.CharField('주문번호', max_length=25,  default='PAYGO' + datetime.now().strftime('%H%M%S%f'))
    # 이쪽 방향으로 가야할 듯 함
    order_number = models.CharField('주문번호', max_length=25, unique=True,
                                    default='PAYGO' + datetime.now().strftime('%H%M%S%f'))
    goods_name = models.CharField('상품 이름', max_length=50)
    # card_name = models.CharField('카드 이름', max_length=20, default='신한 마스터 카드')
    # card_brand = models.CharField('카드 브랜드', max_length=20, default='신한은행')
    card_num = models.CharField('카드숫자', max_length=30)
    card_pwd = models.CharField('카드비밀번호 앞자리 두개', max_length=2)
    card_avail_year = models.CharField('카드 유효 연도', max_length=4)
    card_avail_month = models.CharField('카드_유효_월', max_length=2)
    price = models.PositiveIntegerField('가격')
    # approval_number = models.CharField('승인번호', max_length=100, unique=True)
    status = models.CharField('거래상태', max_length=10, choices=REQUEST_STATUS, default=ON_REQUEST)
    card_quota = models.CharField('할부개월', max_length=2)
    buyer_name = models.CharField('구매자 이름', max_length=20)
    buyer_auth_num = models.CharField('주민등록번호 앞자리', max_length=6)
    buyer_tel = models.CharField('구매자 휴대폰번호', max_length=20)
    buyer_email = models.CharField('구매자 이메일', max_length=50)
    is_canceled = models.BooleanField('취소요청', default=False)
    payed_at = models.DateTimeField('거래시점', auto_now_add=True)
    canceled_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = '결제 내역 정보'
        verbose_name_plural = '%s 목록' % verbose_name
        unique_together = ('paygouser', 'order_number', 'is_canceled')

    def __str__(self):
        return f'유저 : {self.paygouser} | ' \
               f'구매자 정보 : {self.buyer_email if self.buyer_email is not None else self.buyer_tel}'


# 구매자 아이템 모델

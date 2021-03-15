from django.db import models
from datetime import date
from datetime import datetime as dt

from members.models import PayGoUser


class PaymentMethod(models.Model):
    AGENCIES, RELAY = 'ag', 're'
    FRANCHISEE_TYPE = (
        (AGENCIES, 'ag'),
        (RELAY, 're'),
    )

    paygouser = models.ForeignKey(PayGoUser, on_delete=models.PROTECT, related_name='payment_methods', help_text="유저")
    method_type = models.CharField('결제수단', max_length=100)
    service_use_or_not = models.BooleanField('결제서비스 사용여부', blank=True, null=True, default=True)
    service_join_date = models.DateField('서비스등록일', blank=True, null=True, default=date.today)
    store_type = models.CharField('가맹점유형', blank=True, null=True, choices=FRANCHISEE_TYPE, max_length=2,
                                  default=AGENCIES)
    authentication_method = models.CharField('인증방식', blank=True, null=True, max_length=100, default='Keyln')
    partial_cancellation_or_not = models.BooleanField('부분취소사용여부', blank=True, null=True, default=True)
    payment_use_or_not = models.BooleanField('SMS_결제사용여부', blank=True, null=True, default=True)
    shipping_destination_use_or_not = models.BooleanField('배송지사용여부', blank=True, null=True, default=False)
    offline_cat_id = models.CharField('오프라인_CAT_ID', max_length=100, blank=True, null=True)
    card_information_save_use_or_not = models.BooleanField('카드정보저장시사용여부', blank=True, null=True, default=True)
    created_date = models.DateTimeField('생성날짜', auto_now_add=True)
    updated_date = models.DateTimeField('업데이트된날짜', auto_now=True)

    class Meta:
        unique_together = ('paygouser', 'method_type')
        ordering = ['-pk']
        verbose_name = '결제서비스'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'{self.paygouser} | {self.method_type}'


class PaymentMethodSettlementCycle(models.Model):
    NOT_SETTLED, IMMEDIATELY, DAY1, DAY2, DAY3, DAY4, DAY5, DAY6, DAY7, DAY8, DAY9, DAY10, DAY11, DAY12, DAY13, DAY14, \
        DAY15, MONTH1, MONTH2, MONTH3, MONTH4 = 'not_settled', 'immediately', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', \
                                                'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'M1', \
                                                'M2', 'M3', 'M4'
    SETTLEMENT_CYCLE = (
        (NOT_SETTLED, 'not_settled'),
        (IMMEDIATELY, 'immediately'),
        (DAY1, 'D1'),
        (DAY2, 'D2'),
        (DAY3, 'D3'),
        (DAY4, 'D4'),
        (DAY5, 'D5'),
        (DAY6, 'D6'),
        (DAY7, 'D7'),
        (DAY8, 'D8'),
        (DAY9, 'D9'),
        (DAY10, 'D10'),
        (DAY11, 'D11'),
        (DAY12, 'D12'),
        (DAY13, 'D13'),
        (DAY14, 'D14'),
        (DAY15, 'D15'),
        (MONTH1, 'M1'),
        (MONTH2, 'M2'),
        (MONTH3, 'M3'),
        (MONTH4, 'M4'),

    )
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT,
                                       related_name='payment_method_settlement_cycles', help_text="결제수단")
    cycle = models.CharField('정산주기', choices=SETTLEMENT_CYCLE, max_length=20, default=DAY1)
    applied_date = models.DateField('적용일자', default=date.today)
    settlement_wait_time = models.PositiveIntegerField('정산대기시간', blank=True, null=True, default=0)
    affiliate_withdrawal_use_or_not = models.BooleanField('가맹점출금여부', blank=True, null=True, default=False)
    created_date = models.DateTimeField('생성날짜', auto_now_add=True)
    updated_date = models.DateTimeField('업데이트된날짜', auto_now=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = '결제서비스-정산주기 정보'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'{self.cycle} | {self.applied_date}'


# 정산정보
class SettlementInformation(models.Model):
    PRE_CANCEL, POST_CANCEL = 'pre_cancel', 'post_cancel'
    CANCEL_STATUS = (
        (PRE_CANCEL, 'pre_cancel'),
        (POST_CANCEL, 'post_cancel'),
    )
    TRIMMING, ROUNDS = 'trim', 'rounds'
    FEE_STANDARD = (
        (TRIMMING, 'trim'),
        (ROUNDS, 'rounds'),
    )
    CANCEL_POSSIBLE, ONLY_BEFORE_PURCHASE, IMPOSSIBLE = 'cancel_possible', 'only_before_purchase', 'impossible'
    CANCEL_FUNCTION = (
        (CANCEL_POSSIBLE, 'cancel_possible'),
        (ONLY_BEFORE_PURCHASE, 'only_before_purchase'),
        (IMPOSSIBLE, 'impossible'),
    )
    NEXT_DAY, D_DAY = 'next_day', 'd_day',
    SETTLEMENT_TYPE = (
        (NEXT_DAY, 'next_day'),
        (D_DAY, 'd_day'),
    )
    MID_SETTLEMENT, GID_SETTLEMENT = 'mid_settlement', 'gid_settlement',
    SETTLEMENT_METHOD = (
        (MID_SETTLEMENT, 'mid_settlement'),
        (GID_SETTLEMENT, 'gid_settlement'),
    )
    MONTH, OCCASIONAL, SEMIANNUAL, QUARTER, YEAR = 'month', 'occasional', 'semiannual', 'quarter', 'year'
    TAX_BILL_CLASSIFICATION = (
        (MONTH, 'month'),
        (OCCASIONAL, 'occasional'),
        (SEMIANNUAL, 'semiannual'),
        (QUARTER, 'quarter'),
        (YEAR, 'year'),

    )
    APPROVED, CALCULATE, PURCHASE = 'approved', 'calculate', 'purchase'
    TAX_BILL_STANDARD = (
        (APPROVED, 'approved'),
        (CALCULATE, 'calculate'),
        (PURCHASE, 'purchase'),
    )
    paygouser = models.OneToOneField(PayGoUser, on_delete=models.PROTECT, related_name='settlement_informations',
                                     help_text="유저")
    # 에이전시, 가맹점주 각각 null=True 상태에서 각각받아주는 방법도 있다.
    # agency = models.OneToOneField(Agency, on_delete=models.PROTECT,
    #                                  related_name='agency',
    #                                  help_text="에이전시")
    settlement_use_or_not = models.BooleanField('정산사용여부', blank=True, null=True, default=True)
    fee_settlement_standard = models.CharField('수수료정산기준', blank=True, null=True, choices=CANCEL_STATUS, max_length=30,
                                               default=PRE_CANCEL)
    fee_calculation_criteria = models.CharField('수수료계산기준', blank=True, null=True, choices=FEE_STANDARD, max_length=30,
                                                default=TRIMMING)
    fee_registration_criteria = models.BooleanField('수수료등록기준_VAT_포함_or_VAT_미포함', blank=True, null=True, default=True)
    debt_offset_use_or_not = models.BooleanField('채권상계', blank=True, null=True, default=False)
    cancel_function = models.CharField('취소기능', max_length=30, blank=True, null=True, choices=CANCEL_FUNCTION,
                                       default=CANCEL_POSSIBLE)
    settlement_type = models.CharField('정산유형', max_length=30, blank=True, null=True, choices=SETTLEMENT_TYPE,
                                       default=NEXT_DAY)
    settlement_method = models.CharField('정산방법', max_length=30, blank=True, null=True, choices=SETTLEMENT_METHOD,
                                         default=MID_SETTLEMENT)
    restriction_on_cancellation_use_or_not = models.BooleanField('채권방지 취소제한', blank=True, null=True, default=False)
    pending_amount_for_each_case = models.IntegerField('건별지금보류금액', blank=True, null=True, default=0)
    electronic_tax_invoice_email = models.EmailField('전자세금계산서_EMAIL', blank=True, null=True, max_length=100)
    classification_of_issuing_tax_invoices = models.CharField('세금계산서발행구분', max_length=20, blank=True, null=True,
                                                              choices=TAX_BILL_CLASSIFICATION, default=MONTH)
    standard_for_issuance_of_tax_invoice = models.CharField('세금계산서발행기준', max_length=20, blank=True, null=True,
                                                            choices=TAX_BILL_STANDARD, default=CALCULATE)
    created_date = models.DateTimeField('생성날짜', auto_now_add=True)
    updated_date = models.DateTimeField('업데이트된날짜', auto_now=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = '정산정보'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'SettlementInformation 테이블 {self.paygouser} |  {self.settlement_use_or_not}'


# 정산계좌
class SettlementAccount(models.Model):
    settlement_information = models.ForeignKey(SettlementInformation, on_delete=models.PROTECT,
                                               related_name='settlement_account', help_text='정산계좌')
    bank = models.CharField('정산은행', max_length=50)
    account_holder = models.CharField('예금주', max_length=30)
    account_number = models.CharField('계좌번호', max_length=50)
    applied_date = models.DateField('적용일자', blank=True, null=True, default=date.today)
    end_date = models.DateField('종료일자', blank=True, null=True, default=dt(9999, 12, 30))
    created_date = models.DateTimeField('생성날짜', auto_now_add=True)
    updated_date = models.DateTimeField('업데이트된날짜', auto_now=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = '정산계좌 등록'
        verbose_name_plural = '%s 목록' % verbose_name
        unique_together = ['bank', 'account_number']

    def __str__(self):
        # return f' bank_name: {self.bank} | mid : {self.settlement_account}'
        return f' bank_name: {self.bank} | mid :'

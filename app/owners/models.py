from django.db import models
import datetime


class Owner(models.Model):
    CONTACT_IN_CONSULTATION, CONTACT_ACCEPTANCE, CONTACT_RM_REVIEW_REQUEST, CONTACT_RM_REVIEW_COMPLETED, \
        CONTACT_PERSON_IN_CHARGE_APPROVAL_REQUEST, CONTACT_PERSON_IN_CHARGE_APPROVAL_COMPLETED, \
        CONTACT_PERSON_IN_CHARGE_APPROVAL_REJECT, CONTACT_COMPLETION = 'ct_consult', 'ct_accept', 'rm_req', 'rm_comp', \
                                                                       'approve_req', 'approve_comp', \
                                                                       'approve_reject', 'contact_comp '
    CONTACT_STATUS = (
        (CONTACT_IN_CONSULTATION, '상담중'),
        (CONTACT_ACCEPTANCE, '계약서접수'),
        (CONTACT_RM_REVIEW_REQUEST, 'RM_심사요청'),
        (CONTACT_RM_REVIEW_COMPLETED, 'RM_심사완료'),
        (CONTACT_PERSON_IN_CHARGE_APPROVAL_REQUEST, '책임자승인요청'),
        (CONTACT_PERSON_IN_CHARGE_APPROVAL_COMPLETED, '책임자승인완료'),
        (CONTACT_PERSON_IN_CHARGE_APPROVAL_REJECT, '책임자승인반려'),
        (CONTACT_COMPLETION, '계약완료'),
    )
    # 가맹점 정보
    business_license_number = models.CharField("사업자등록번호", max_length=100, unique=True)
    business_store_type = models.CharField("가게종목", max_length=30, default="전자상거래")
    business_condition = models.CharField("업태", max_length=30, default="서비스")
    business_open_date = models.DateField("사업개시일", blank=True, null=True)
    business_capital_amount = models.IntegerField("사업자본금", blank=True, null=True)
    business_url = models.URLField("가맹점_URL", blank=True, null=True)
    business_representative_name = models.CharField('대표자명', max_length=100, blank=True, null=True)
    business_representative_birth = models.DateField("대표자생년월일", blank=True, null=True)
    corporate_registration_number = models.CharField("법인등록번호", max_length=100, blank=True, null=True)
    business_representative_phone = models.CharField("대표자_TEL", max_length=100, blank=True, null=True)
    business_representative_fax = models.CharField("대표자_FAX", max_length=100, blank=True, null=True)
    business_representative_email = models.EmailField("대표자_EMAIL", max_length=255, blank=True, null=True)
    # 필수 항목
    joined_date = models.DateField("접수일", auto_now_add=True)
    business_classification = models.CharField("사업체구분", max_length=100)
    business_name = models.CharField("상호명", max_length=100)
    business_main_item = models.CharField('주요판매물품', max_length=100)
    application_route = models.CharField("접수경로", max_length=100, )
    sales_channel = models.CharField("영업채널", max_length=100, blank=True)
    # 미 필수 항목
    transaction_amount = models.IntegerField("거래금액", blank=True, null=True)
    past_pg_company = models.CharField("기존_PG사", max_length=100, blank=True)
    business_official_address = models.CharField('사업장소재지', max_length=100, blank=True)
    business_real_address = models.CharField('실사업장주소', max_length=100, blank=True)
    initial_registration_fee = models.IntegerField("초기등록비", default=0)
    annual_management_fee = models.IntegerField("연_관리비", default=0)
    guarantee_insurance_policy = models.BooleanField("보증보험증권", default=True)
    reason_exemption = models.TextField("면제사유", default="")
    call_contents = models.TextField("통화내역", default="")
    contact_date_year_month = models.DateField("계약일자", default=datetime.date.today)
    # 계약 예정월 (월까지 표시하도록)
    contact_date_month = models.DateField("계약예정월", default=datetime.date.today)
    contact_receipt = models.BooleanField("계약서_수취", default=False)
    contact_current_status = models.CharField("계약현재상태", max_length=15, choices=CONTACT_STATUS,
                                              default=CONTACT_IN_CONSULTATION)
    contact_type = models.CharField("계약서종류", max_length=100, default="일반")
    pdf1 = models.FileField('PDF1', upload_to='users/pdf', blank=True, null=True)
    updated_date = models.DateTimeField('업데이트된날짜', auto_now=True)
    pay_managers = models.ManyToManyField('PayGoComputationalManager', through='ConnectOwnerManager',
                                          blank=True,
                                          help_text='사업자관리자')

    class Meta:
        ordering = ['-pk']
        verbose_name = '사업자'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'{self.business_license_number} {self.business_name} '


class ConnectOwnerManager(models.Model):
    manager = models.ForeignKey('PayGoComputationalManager', related_name='manager_to_owner',
                                on_delete=models.PROTECT, help_text='매니저')
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, related_name='owner_to_manager', help_text='사업자')
    created_date = models.DateTimeField('생성날짜', auto_now_add=True)

    def __str__(self):
        return f'{self.owner} {self.manager}'


class PayGoComputationalManager(models.Model):
    name = models.CharField('담당자이름', max_length=100)
    department = models.CharField('담당자부서', max_length=100)
    position = models.CharField('담당자직책', max_length=100)
    phone_number = models.CharField('담당자핸드폰번호', max_length=100, )
    email = models.EmailField("담당자_EMAIL", max_length=255)
    created_date = models.DateTimeField('생성날짜', auto_now_add=True)
    updated_date = models.DateTimeField('업데이트된날짜', auto_now=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = '담당영업자'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        return f'pay go computation manager {self.department} {self.name}'

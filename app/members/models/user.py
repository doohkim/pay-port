from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class PayGoUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수항목입니다')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        # user required 필드에 없으면 owner 받을 수 없음
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('type', PayGoUser.TYPE_STAFF)
        # owner 관리자 추가 admin 유저도 사업자 등록을 해야하는데 여기서 에러나서
        # extra_fields.setdefault('owner', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class PayGoUser(AbstractUser):
    TYPE_STAFF, TYPE_AGENCY, TYPE_FRANCHISEE = 's', 'a', 'f'
    CHOICES_TYPE = (
        (TYPE_FRANCHISEE, '가맹점'),
        (TYPE_AGENCY, '에이전시'),
        (TYPE_STAFF, '관리자'),
    )
    username = None
    # 아이디
    mid = models.CharField("가맹점아이디_MID", unique=True, max_length=10)
    gid = models.CharField("가맹점아이디_GID", max_length=10)
    # 로그인시 노출 되는 이름
    mid_name = models.CharField("가맹점관리자_MID_name", max_length=9)
    main_homepage = models.URLField("메인홈페이지_URL", blank=True, null=True),
    sub_homepage = models.URLField("서브몰심사_URL", blank=True, null=True)
    # 아이디 활성화 여부
    is_active = models.BooleanField('활성화여부', default=True)
    type = models.CharField('타입', max_length=1, choices=CHOICES_TYPE, default=TYPE_FRANCHISEE)
    email = models.EmailField('이메일', max_length=100)
    phone_number = models.CharField('전화번호', max_length=30, blank=True, null=True)
    fax_number = models.CharField("팩스번호", max_length=30, blank=True, null=True)
    store_joined_date = models.DateField("가맹점등록일자", auto_now_add=True)
    store_modified_date = models.DateField("루멘페이고전산업데이트일", auto_now=True)
    transfer_or_not = models.BooleanField('이관여부', default=False)
    published_or_not = models.BooleanField('수도여부', default=False)
    pay_link_or_not = models.BooleanField('페이링크여부', default=False)
    pg_info_auto_save_or_not = models.BooleanField('PG_정보자동저장', default=False)
    delivery_pay_or_not = models.BooleanField('딜리버리페이여부', default=False)

    # 사업자 | 나중에 필수값으로 설정 해주자!
    owners = models.ForeignKey('owners.Owner', on_delete=models.PROTECT, null=True, blank=True,
                               related_name='paygousers', help_text='사업자번호등록')
    # 에이전트
    agencies = models.ForeignKey('self', on_delete=models.PROTECT, related_name='franchisee_to_agency',
                                 verbose_name='가맹점 소개 시킨 에이전트 목록', blank=True, null=True, help_text='에이전트')
    # 담당자
    # 그리고 M2M은 related_name 뭐라고 적어야 하지?
    # related_name 과 변수명이 같아야 하는가?
    pay_managers = models.ManyToManyField('owners.PayGoComputationalManager', blank=True,
                                          through='ConnectPayGoUserManager', help_text="전산 관리자")
    # settlement_account = models.ForeignKey('paymethod.SettlementAccount', on_delete=models.PROTECT, blank=True,
    #                                        null=True, related_name='paygousers', help_text='정산계좌등록')

    # paymentmethod = models.ManyToManyField('paymethod.PaymentMethod', related_name='paygousers', help_text="결제서비스정보")

    USERNAME_FIELD = 'mid'
    REQUIRED_FIELDS = ['email', ]

    objects = PayGoUserManager()

    class Meta:
        ordering = ['-pk']
        verbose_name = '관리자'
        verbose_name_plural = '%s 목록' % verbose_name

    def __str__(self):
        if self.type == self.TYPE_STAFF:
            return f'[관리자유저] {self.mid_name} | 전화번호 : {self.phone_number}'
        elif self.type == self.TYPE_FRANCHISEE:
            return f'[가맹점유저] {self.mid_name} | 전화번호 : {self.phone_number} '
        elif self.type == self.TYPE_AGENCY:
            return f'[에이전시유저] {self.mid_name} | 전화번호 : {self.phone_number} '
        return f'{self.mid} | 로그인시 : {self.mid_name}'


class ConnectPayGoUserManager(models.Model):
    manager = models.ForeignKey('owners.PayGoComputationalManager', related_name='manager_to_user',
                                on_delete=models.PROTECT, help_text='매니저')
    user = models.ForeignKey(PayGoUser, related_name='user_to_manager', on_delete=models.PROTECT,
                             help_text="페이고유저")
    created_date = models.DateField('생성날짜', auto_now_add=True)

    def __str__(self):
        return f'{self.user} | {self.manager}'

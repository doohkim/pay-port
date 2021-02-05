# Generated by Django 2.2.17 on 2021-02-02 12:15

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method_type', models.CharField(max_length=100, verbose_name='결제수단')),
                ('service_use_or_not', models.BooleanField(default=True, verbose_name='결제서비스 사용여부')),
                ('service_join_date', models.DateField(default=datetime.date.today, verbose_name='서비스등록일')),
                ('store_type', models.CharField(choices=[('ag', 'ag'), ('re', 're')], default='ag', max_length=2, verbose_name='가맹점유형')),
                ('authentication_method', models.CharField(default='Keyln', max_length=100, verbose_name='인증방식')),
                ('partial_cancellation_or_not', models.BooleanField(default=True, verbose_name='부분취소사용여부')),
                ('payment_use_or_not', models.BooleanField(default=True, verbose_name='SMS_결제사용여부')),
                ('shipping_destination_use_or_not', models.BooleanField(default=False, verbose_name='배송지사용여부')),
                ('offline_cat_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='오프라인_CAT_ID')),
                ('card_information_save_use_or_not', models.BooleanField(default=True, verbose_name='카드정보저장시사용여부')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='업데이트된날짜')),
                ('paygouser', models.ForeignKey(help_text='가맹점주', on_delete=django.db.models.deletion.PROTECT, related_name='paymentmethods', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '결제서비스',
                'verbose_name_plural': '결제서비스 목록',
                'ordering': ['-pk'],
                'unique_together': {('paygouser', 'method_type')},
            },
        ),
        migrations.CreateModel(
            name='SettlementInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settlement_use_or_not', models.BooleanField(default=True, verbose_name='정산사용여부')),
                ('fee_settlement_standard', models.CharField(choices=[('pre_cancel', 'pre_cancel'), ('post_cancel', 'post_cancel')], default='pre_cancel', max_length=30, verbose_name='수수료정산기준')),
                ('fee_calculation_criteria', models.CharField(choices=[('trim', 'trim'), ('rounds', 'rounds')], default='trim', max_length=30, verbose_name='수수료계산기준')),
                ('fee_registration_criteria', models.BooleanField(default=True, verbose_name='수수료등록기준_VAT포함_or_VAT미포함')),
                ('debt_offset_use_or_not', models.BooleanField(default=False, verbose_name='채권상계')),
                ('cancel_function', models.CharField(choices=[('cancel_possible', 'cancel_possible'), ('only_before_purchase', 'only_before_purchase'), ('impossible', 'impossible')], default='cancel_possible', max_length=30, verbose_name='취소기능')),
                ('settlement_type', models.CharField(choices=[('next_day', 'next_day'), ('d_day', 'd_day')], default='next_day', max_length=30, verbose_name='정산유형')),
                ('settlement_method', models.CharField(choices=[('mid_settlement', 'mid_settlement'), ('gid_settlement', 'gid_settlement')], default='mid_settlement', max_length=30, verbose_name='정산방법')),
                ('restriction_on_cancellation_use_or_not', models.BooleanField(default=False, verbose_name='채권방지 취소제한')),
                ('pending_amount_for_each_case', models.IntegerField(default=0, verbose_name='건별지금보류금액')),
                ('electronic_tax_invoice_email', models.EmailField(max_length=100, verbose_name='전자세금계산서_EMAIL')),
                ('classification_of_issuing_tax_invoices', models.CharField(choices=[('month', 'month'), ('occasional', 'occasional'), ('semiannual', 'semiannual'), ('quarter', 'quarter'), ('year', 'year')], default='month', max_length=20, verbose_name='세금계산서발행구분')),
                ('standard_for_issuance_of_tax_invoice', models.CharField(choices=[('approved', 'approved'), ('calculate', 'calculate'), ('purchase', 'purchase')], default='calculate', max_length=20, verbose_name='세금계산서발행기준')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='업데이트된날짜')),
                ('paygouser', models.OneToOneField(help_text='가맹점주', on_delete=django.db.models.deletion.PROTECT, related_name='paygouser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '정산정보',
                'verbose_name_plural': '정산정보 목록',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='SettlementAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=50, verbose_name='정산은행')),
                ('account_holder', models.CharField(max_length=30, verbose_name='예금주')),
                ('account_number', models.CharField(max_length=50, verbose_name='계좌번호')),
                ('applied_date', models.DateField(default=datetime.date.today, verbose_name='적용일자')),
                ('end_date', models.DateField(default=datetime.datetime(9999, 12, 30, 0, 0), verbose_name='종료일자')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='업데이트된날짜')),
                ('settlementinformation', models.ForeignKey(help_text='정산계좌', on_delete=django.db.models.deletion.PROTECT, related_name='settlementaccount', to='paymethod.SettlementInformation')),
            ],
            options={
                'verbose_name': '정산계좌 등록',
                'verbose_name_plural': '정산계좌 등록 목록',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='PaymentMethodSettlementCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycle', models.CharField(choices=[('not_settled', 'not_settled'), ('immediately', 'immediately'), ('D1', 'D1'), ('D2', 'D2'), ('D3', 'D3'), ('D4', 'D4'), ('D5', 'D5'), ('D6', 'D6'), ('D7', 'D7'), ('D8', 'D8'), ('D9', 'D9'), ('D10', 'D10'), ('D11', 'D11'), ('D12', 'D12'), ('D13', 'D13'), ('D14', 'D14'), ('D15', 'D15'), ('M1', 'M1'), ('M2', 'M2'), ('M3', 'M3'), ('M4', 'M4')], default='D1', max_length=20, verbose_name='정산주기')),
                ('applied_date', models.DateField(default=datetime.date.today, verbose_name='적용일자')),
                ('settlement_wait_time', models.PositiveIntegerField(default=0, verbose_name='정산대기시간')),
                ('affiliate_withdrawal_use_or_not', models.BooleanField(default=False, verbose_name='가맹점출금여부')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='업데이트된날짜')),
                ('paymentmethodsettlementcycles', models.ForeignKey(help_text='가맹점주', on_delete=django.db.models.deletion.PROTECT, related_name='paymentmethodsettlementcycles', to='paymethod.PaymentMethod')),
            ],
            options={
                'verbose_name': '결제서비스-정산주기 정보',
                'verbose_name_plural': '결제서비스-정산주기 정보 목록',
                'ordering': ['-pk'],
            },
        ),
    ]
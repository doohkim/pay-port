from django.db import transaction
from rest_framework.serializers import ModelSerializer

from paymethod.exceptions import SettlementAccountBadRequestException, SettlementInformationCreateBadRequestException, \
    SettlementInformationUpdateBadRequestException
from paymethod.models import SettlementAccount, SettlementInformation

# 유저 정산 계좌 리스트
from paymethod.serializers.serializer_instance_update_functions import settlement_info_serializer_update_method


class SettlementAccountSerializer(ModelSerializer):
    class Meta:
        model = SettlementAccount
        fields = '__all__'


# 유저 정산정보 리스트
class SettlementInformationSerializer(ModelSerializer):
    settlement_account = SettlementAccountSerializer(many=True, required=False)

    class Meta:
        model = SettlementInformation
        fields = '__all__'


# 유저 정산 계좌 Create
class SettlementAccountCreateSerializer(ModelSerializer):
    class Meta:
        model = SettlementAccount

        fields = (
            'bank',
            'account_holder',
            'account_number',
            'applied_date',
            'end_date'
        )

    def validate(self, attrs):
        # 계좌번호에 1004 넣고 취소하는 작업 필요!
        print('계좌번호 확인 필요? 유저 정산계좌 테이블', attrs)
        # if SettlementAccount.objects.filter(account_number=attrs['account_number']).exists():
        #     raise serializers.ValidationError({'account_number': 'account_number already exist'})
        return attrs

    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []


# 유저 정산정보 Create
class SettlementInformationCreateSerializer(ModelSerializer):
    settlement_account = SettlementAccountCreateSerializer(many=True, required=False)

    class Meta:
        model = SettlementInformation
        fields = (
            'settlement_account',
            'settlement_use_or_not',
            'fee_settlement_standard',
            'fee_calculation_criteria',
            'fee_registration_criteria',
            'debt_offset_use_or_not',
            'cancel_function',
            'settlement_type',
            'settlement_method',
            'restriction_on_cancellation_use_or_not',
            'pending_amount_for_each_case',
            'electronic_tax_invoice_email',
            'classification_of_issuing_tax_invoices',
            'standard_for_issuance_of_tax_invoice',
            'fee_settlement_standard',
        )

    @transaction.atomic()
    def create(self, validated_data):
        settlement_account_data = validated_data.pop('settlement_account')
        print(settlement_account_data)
        try:
            # get_or_create 로 다시 만들기를 하였을 때 버그가 안나게 할 수 있지만
            # 일부러 업데이트 방향으로 이끌기 위해 버그를 만들어 주었다.
            settlement_information = SettlementInformation.objects.create(
                paygouser=validated_data['paygouser'],
                electronic_tax_invoice_email=validated_data.get('electronic_tax_invoice_email', None),
                settlement_use_or_not=validated_data.get('settlement_use_or_not', None),
                fee_settlement_standard=validated_data.get('fee_settlement_standard', None),
                fee_calculation_criteria=validated_data.get('fee_calculation_criteria', None),
                fee_registration_criteria=validated_data.get('fee_registration_criteria', None),
                debt_offset_use_or_not=validated_data.get('debt_offset_use_or_not', None),
                cancel_function=validated_data.get('cancel_function', None),
                settlement_type=validated_data.get('settlement_type', None),
                settlement_method=validated_data.get('settlement_method', None),
                restriction_on_cancellation_use_or_not=validated_data.get('restriction_on_cancellation_use_or_not',
                                                                          None),
                pending_amount_for_each_case=validated_data.get('pending_amount_for_each_case', None),
                classification_of_issuing_tax_invoices=validated_data.get('classification_of_issuing_tax_invoices',
                                                                          None),
                standard_for_issuance_of_tax_invoice=validated_data.get('standard_for_issuance_of_tax_invoice',
                                                                        None),
            )
        except Exception as e:
            print('정산정보 만들때 에러', e)
            raise SettlementInformationCreateBadRequestException
        try:
            if settlement_account_data:
                for account_data in settlement_account_data:
                    SettlementAccount.objects.get_or_create(
                        bank=account_data.get('bank', None),
                        account_holder=account_data.get('account_holder', None),
                        account_number=account_data.get('account_number', None),
                        applied_date=account_data.get('applied_date', None),
                        end_date=account_data.get('end_date', None),
                        settlement_information=settlement_information,
                    )
        except Exception as e:
            print('정산계좌 만들 때 에러', e)
            raise SettlementAccountBadRequestException
        return settlement_information


# 유저 정산 계좌 Update
class SettlementAccountUpdateSerializer(ModelSerializer):
    class Meta:
        model = SettlementAccount
        fields = (
            'bank',
            'account_holder',
            'account_number',
            'applied_date',
            'end_date'
        )

    def validated(self, attrs):
        # 계좌번호에 1004 넣고 취소하는 작업 필요!
        print('계좌번호 확인 필요?')
        return attrs

    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []


# 유저 정산정보 Update
class SettlementInformationUpdateSerializer(ModelSerializer):
    settlement_account = SettlementAccountUpdateSerializer(many=True, required=False)

    class Meta:
        model = SettlementInformation
        fields = (
            'settlement_account',
            'settlement_use_or_not',
            'fee_settlement_standard',
            'fee_calculation_criteria',
            'fee_registration_criteria',
            'debt_offset_use_or_not',
            'cancel_function',
            'settlement_type',
            'settlement_method',
            'restriction_on_cancellation_use_or_not',
            'pending_amount_for_each_case',
            'electronic_tax_invoice_email',
            'classification_of_issuing_tax_invoices',
            'standard_for_issuance_of_tax_invoice',
            'fee_settlement_standard',
        )

    @transaction.atomic()
    def update(self, instance, validated_data):
        settlement_account_data = validated_data.pop('settlement_account')
        try:
            settlement_info_instance = settlement_info_serializer_update_method(instance, validated_data)
        except Exception:
            raise SettlementInformationUpdateBadRequestException
        try:
            if settlement_account_data:
                for account_data in settlement_account_data:
                    SettlementAccount.objects.get_or_create(
                        bank=account_data.get('bank', None),
                        account_holder=account_data.get('account_holder', None),
                        account_number=account_data.get('account_number', None),
                        applied_date=account_data.get('applied_date', None),
                        end_date=account_data.get('end_date', None),
                        settlement_information=settlement_info_instance,
                    )
        except Exception as e:
            print('정산계좌 update 에러', e)
            raise SettlementAccountBadRequestException
        return settlement_info_instance


# 유저 정산 계좌 Retrieve
class SettlementAccountDetailSerializer(ModelSerializer):
    class Meta:
        model = SettlementAccount
        fields = (
            'bank',
            'account_holder',
            'account_number',
            'applied_date',
            'end_date'
        )


# 유저 정산정보 Retrieve
class SettlementInformationDetailSerializer(ModelSerializer):
    settlement_account = SettlementAccountCreateSerializer(many=True, required=False)

    class Meta:
        model = SettlementInformation
        fields = (
            'settlement_account',
            'paygouser',
            'settlement_use_or_not',
            'fee_settlement_standard',
            'fee_calculation_criteria',
            'fee_registration_criteria',
            'debt_offset_use_or_not',
            'cancel_function',
            'settlement_type',
            'settlement_method',
            'restriction_on_cancellation_use_or_not',
            'pending_amount_for_each_case',
            'electronic_tax_invoice_email',
            'classification_of_issuing_tax_invoices',
            'standard_for_issuance_of_tax_invoice',
            'fee_settlement_standard',
        )

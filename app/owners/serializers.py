from django.db import transaction

from rest_framework.serializers import ModelSerializer

from common import check_owner_number
from members.serializer_method_override import pay_go_manager_update_method
from .excepts import BusinessLicenseNumberException, NotFoundManagerNumberException
from .models import Owner, PayGoComputationalManager, ConnectOwnerManager
from .serializer_method_override import owner_serializer_update_method


class PayGoComputationalManagerCreateSerializer(ModelSerializer):
    class Meta:
        model = PayGoComputationalManager
        fields = ('name', 'department', 'position', 'position', 'phone_number', 'email')


# 사업자 번호 등록 및 List && Create Serializer
class OwnerSerializer(ModelSerializer):
    pay_managers = PayGoComputationalManagerCreateSerializer(many=True, required=False)

    class Meta:
        model = Owner
        # fields = ('business_license_number', 'business_classification', 'business_name', 'business_main_item',
        #           'application_route', 'sales_channel', 'pay_managers', 'call_contents')
        fields = '__all__'

    def validate(self, data):
        """
            Check that the business license number not including String en or hangul
            사업자 번호에 한글이나 영어가 포함되지 않도록 확인하자
            정규표현식으로 구분할 수 있음
        """
        business_license_number = data['business_license_number']
        result, boolean_result = check_owner_number(business_license_number)
        if boolean_result:
            # 모델에 데이터 필드 추가하기
            data['call_contents'] = result
            return data
        else:
            raise BusinessLicenseNumberException

    @transaction.atomic()
    def create(self, validated_data):
        # print(validated_data)
        pay_managers_data = validated_data.pop('pay_managers', None)
        # print('pay_managers_data', pay_managers_data)
        owner = Owner.objects.create(**validated_data)
        if pay_managers_data:
            for manager in pay_managers_data:
                manager_obj, _ = PayGoComputationalManager.objects.get_or_create(
                    name=manager['name'],
                    department=manager['department'],
                    position=manager['position'],
                    phone_number=manager['phone_number'],
                    email=manager['email']
                )
                ConnectOwnerManager.objects.create(manager=manager_obj, owner=owner)
        return owner

    @transaction.atomic()
    def update(self, instance, validated_data):
        pay_managers = validated_data.pop('pay_managers', None)
        owner = owner_serializer_update_method(instance, validated_data)
        owner.save()
        if pay_managers:
            for manager in pay_managers:
                manager_phone_number = manager.get('phone_number', None)
                # 아이디가 넘어 왔다면
                if manager_phone_number:
                    manager_obj = PayGoComputationalManager.objects.get(phone_number=manager_phone_number)
                    manager_instance = pay_go_manager_update_method(manager_obj, manager)
                    manager_instance.save()
                    ConnectOwnerManager.objects.get_or_create(manager=manager_instance, owner=owner)
                else:
                    raise NotFoundManagerNumberException
                    # serializer = PayGoComputationalManagerCreateSerializer(data=manager)
                    # if serializer.is_valid(raise_exception=True):
                    #     serializer.save()
                    #     manager_obj = PayGoComputationalManager.objects.get(phone_number=serializer.data['phone_number'])
                    #     ConnectOwnerManager.objects.create(manager=manager_obj, owner=owner)
        return instance


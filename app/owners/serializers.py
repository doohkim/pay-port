from django.db import transaction

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Owner, PayGoComputationalManager, ConnectOwnerManager


class PayGoComputationalManagerSerializer(ModelSerializer):
    class Meta:
        model = PayGoComputationalManager
        fields = '__all__'


class OwnerSerializer(ModelSerializer):
    pay_managers = PayGoComputationalManagerSerializer(many=True)

    class Meta:
        model = Owner
        fields = '__all__'


class PayGoComputationalManagerCreateSerializer(ModelSerializer):
    class Meta:
        model = PayGoComputationalManager
        fields = ('name', 'department', 'position', 'position', 'phone_number', 'email')


class OwnerCreateSerializer(ModelSerializer):
    pay_managers = PayGoComputationalManagerCreateSerializer(many=True, write_only=True, )

    class Meta:
        model = Owner
        fields = ('business_license_number', 'business_classification', 'business_name', 'business_main_item',
                  'application_route', 'sales_channel', 'pay_managers',)

    @transaction.atomic()
    def create(self, validated_data):
        print(validated_data)
        pay_managers_data = validated_data.pop('pay_managers', None)
        print('pay_managers_data', pay_managers_data)
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

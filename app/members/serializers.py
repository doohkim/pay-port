from django.db import transaction

from rest_framework import serializers

from members.models import FranchiseeUser, Memo, ConnectPayGoUserManager
from owners.models import PayGoComputationalManager


class PayGoComputationalManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayGoComputationalManager
        fields = '__all__'


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = '__all__'


class FranchiseeUserSerializer(serializers.ModelSerializer):
    memos = MemoSerializer(many=True, required=False)
    franchisee_managers = PayGoComputationalManagerSerializer(many=True, required=False)

    class Meta:
        model = FranchiseeUser
        fields = '__all__'


# Create
class PayGoComputationalManagerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayGoComputationalManager
        fields = ('name', 'department', 'position', 'phone_number', 'email')


class MemoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ('sales_slip', 'vat_notation', 'payment_notice', 'modify_text')


class FranchiseeUserManagerCreateSerializer(serializers.ModelSerializer):
    memos = MemoCreateSerializer(many=True, required=False, write_only=True)
    franchisee_managers = PayGoComputationalManagerCreateSerializer(many=True, write_only=True)

    class Meta:
        model = FranchiseeUser
        fields = (
            'mid',
            'gid',
            'mid_name',
            'main_homepage',
            'sub_homepage',
            'is_active',
            "password",
            # 'user_type',
            'boss_name',
            'email',
            'phone_number',
            'fax_number',
            'transfer_or_not',
            'published_or_not',
            'pay_link_or_not',
            'pg_info_auto_save_or_not',
            'delivery_pay_or_not',
            'memos',
            'franchisee_managers',
        )

    @transaction.atomic()
    def create(self, validated_data):
        franchisee_managers_data = validated_data.pop('franchisee_managers', None)
        memos_data = validated_data.pop('memos', None)
        franchisee_user = FranchiseeUser.objects.create(**validated_data)

        if memos_data:
            for memo in memos_data:
                memo, _ = Memo.objects.get_or_create(
                    franchisee_user=franchisee_user,
                    modify_text=memo['modify_text']
                )
                print(memo)

        if franchisee_managers_data:
            for manager in franchisee_managers_data:
                manager_obj, _ = PayGoComputationalManager.objects.get_or_create(
                    name=manager['name'],
                    department=manager['department'],
                    position=manager['position'],
                    phone_number=manager['phone_number'],
                    email=manager['email']
                )
                connect_user_manager = ConnectPayGoUserManager.objects.create(manager=manager_obj, user=franchisee_user)
                print(connect_user_manager)
        return franchisee_user

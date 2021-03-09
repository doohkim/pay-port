from django.db import transaction

from rest_framework import serializers

from members.models import FranchiseeUser, Memo, ConnectPayGoUserManager
from members.serializer_method_override import franchisee_update_method, pay_go_manager_update_method
from owners.excepts import NotFoundManagerNumberException
from owners.models import PayGoComputationalManager


class PayGoComputationalManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayGoComputationalManager
        fields = '__all__'


class MemoSerializer(serializers.ModelSerializer):
    franchisee_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Memo
        fields = '__all__'


class FranchiseeUserSerializer(serializers.ModelSerializer):
    # 읽기와 쓰기 모두 쓰기 위해서 many=True 로 값을 받고 보내줄것 임
    # client 쪽에서 리스트 형태로 보내줘야 합니다.(request)
    memos = MemoSerializer(many=True, required=False)
    franchisee_managers = PayGoComputationalManagerSerializer(many=True, required=False)

    class Meta:
        model = FranchiseeUser
        fields = '__all__'

    @transaction.atomic()
    def create(self, validated_data):
        franchisee_managers_data = validated_data.pop('franchisee_managers', None)
        memos_data = validated_data.pop('memos', None)
        franchisee_user = FranchiseeUser.objects.create(**validated_data)
        franchisee_user.set_password(validated_data['password'])
        franchisee_user.save()
        # 만약 하나만 받는다면 detail view와 다 따로 만들어 줘야 함
        if memos_data:
            for memo in memos_data:
                memo, _ = Memo.objects.get_or_create(
                    # self.requests.user 로 바꿔주자
                    franchisee_user=franchisee_user,
                    sales_slip=memo.get('sales_slip', None),
                    vat_notation=memo.get('vat_notation', None),
                    payment_notice=memo.get('payment_notice', None),
                    modify_text=memo.get('modify_text', None),

                )
        if franchisee_managers_data:
            for manager in franchisee_managers_data:
                manager_obj, _ = PayGoComputationalManager.objects.get_or_create(
                    name=manager.get('name', None),
                    department=manager.get('department', None),
                    position=manager.get('position', None),
                    phone_number=manager.get('phone_number', None),
                    email=manager.get('email', None),
                )
                ConnectPayGoUserManager.objects.create(manager=manager_obj, user=franchisee_user)
        return franchisee_user

    @transaction.atomic()
    def update(self, instance, validated_data):
        franchisee_managers_data = validated_data.pop('franchisee_managers', None)
        memos_data = validated_data.pop('memos', None)
        f_user = franchisee_update_method(instance, validated_data)
        if franchisee_managers_data:
            for manager in franchisee_managers_data:
                manager_phone_number = manager.get('phone_number', None)
                if manager_phone_number:
                    manager_obj = PayGoComputationalManager.objects.get(phone_number=manager_phone_number)
                    manager_instance = pay_go_manager_update_method(manager_obj, manager)
                    manager_instance.save()
                    ConnectPayGoUserManager.objects.get_or_create(manager=manager_instance, user=f_user)
                else:
                    raise NotFoundManagerNumberException
        if memos_data:
            for memo in memos_data:
                Memo.objects.create(
                    # self.requests.user 로 바꿔주자
                    franchisee_user=f_user,
                    sales_slip=memo.get('sales_slip', None),
                    vat_notation=memo.get('vat_notation', None),
                    payment_notice=memo.get('payment_notice', None),
                    modify_text=memo.get('modify_text', None),
                )
        return f_user

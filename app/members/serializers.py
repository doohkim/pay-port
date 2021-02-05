from rest_framework import serializers

from members.models import FranchiseeUser, Memo
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
    pay_managers = PayGoComputationalManagerSerializer(many=True)

    class Meta:
        model = FranchiseeUser
        fields = '__all__'

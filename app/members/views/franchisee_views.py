from rest_framework import generics
from rest_framework.generics import get_object_or_404

from members.models import FranchiseeUser
from members.serializers import FranchiseeUserSerializer


class FranchiseeUserListCreateView(generics.ListCreateAPIView):
    queryset = FranchiseeUser.objects.all()
    serializer_class = FranchiseeUserSerializer


class FranchiseeUserDetailView(generics.RetrieveAPIView):
    queryset = FranchiseeUser.objects.all()
    serializer_class = FranchiseeUserSerializer

    def get_object(self):
        f_user = get_object_or_404(FranchiseeUser, pk=self.kwargs['pk'])
        return f_user


class FranchiseeUserUpdateView(generics.UpdateAPIView):
    queryset = FranchiseeUser.objects.all()
    serializer_class = FranchiseeUserSerializer

    def get_object(self):
        # requests.user로 수정 할 예정
        obj = get_object_or_404(FranchiseeUser, mid=self.request.data['mid'])
        return obj

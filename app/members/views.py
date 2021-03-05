from rest_framework import generics

from members.models import FranchiseeUser
from members.serializers import FranchiseeUserSerializer, FranchiseeUserManagerCreateSerializer


class FranchiseeUserListCreateView(generics.ListCreateAPIView):
    queryset = FranchiseeUser.objects.get_queryset()[0:20]
    serializer_class = FranchiseeUserSerializer


class FranchiseeUserCreateView(generics.CreateAPIView):
    queryset = FranchiseeUser.objects.get_queryset()
    serializer_class = FranchiseeUserManagerCreateSerializer

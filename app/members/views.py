from rest_framework import generics

from members.models import FranchiseeUser
from members.serializers import FranchiseeUserSerializer


class FranchiseeUserListCreateView(generics.ListCreateAPIView):
    queryset = FranchiseeUser.objects.get_queryset()
    serializer_class = FranchiseeUserSerializer

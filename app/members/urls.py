from django.urls import path
from .views import FranchiseeUserListCreateView, FranchiseeUserCreateView

urlpatterns = [
    path('list/', FranchiseeUserListCreateView.as_view(),),
    path('create/', FranchiseeUserCreateView.as_view())
]

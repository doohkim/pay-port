from django.urls import path
from .views import FranchiseeUserListCreateView

urlpatterns = [
    path('list/', FranchiseeUserListCreateView.as_view(),)
]

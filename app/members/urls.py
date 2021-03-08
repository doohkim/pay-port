from django.urls import path
from .views import FranchiseeUserListCreateView, FranchiseeUserDetailView, FranchiseeUserUpdateView

urlpatterns = [
    # 가맹점주 리스트
    path('franchisee/list/', FranchiseeUserListCreateView.as_view(),),
    path('franchisee/create/', FranchiseeUserListCreateView.as_view(),),
    path('franchisee/detail/<int:pk>/', FranchiseeUserDetailView.as_view(), ),
    path('franchisee/update/', FranchiseeUserUpdateView.as_view(), ),

    # path('franchisee/create/', FranchiseeUserCreateView.as_view()),


]

from django.urls import path
from .views import FranchiseeUserListCreateView, FranchiseeUserDetailView, FranchiseeUserUpdateView
from .views.normal_user_views import AuthTokenAPIVIew, PwdResetEmailAPIView, TokenSendEmailAPIView, \
    AuthUserLoginView, UserLogoutAPIView, UserDetailAPIView, RegisterAPIView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [

    # 가맹점주 리스트
    path('franchisee/list/', FranchiseeUserListCreateView.as_view(), ),
    path('franchisee/create/', FranchiseeUserListCreateView.as_view(), ),
    path('franchisee/detail/<int:pk>/', FranchiseeUserDetailView.as_view(), ),
    path('franchisee/update/', FranchiseeUserUpdateView.as_view(), ),

    # 회원가입
    path('normal/register/', RegisterAPIView.as_view()),
    # 로그인 1
    path('normal/login/', AuthTokenAPIVIew.as_view()),
    # 로그인 2(평상시 확정)
    path('normal/user/', AuthUserLoginView.as_view()),

    # 비밀번호 변경
    path('normal/send/', TokenSendEmailAPIView.as_view()),
    path('normal/pwdchange/', PwdResetEmailAPIView.as_view()),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('normal/detail/', UserDetailAPIView.as_view()),
    # logout url
    path('logout/', UserLogoutAPIView.as_view()),

]

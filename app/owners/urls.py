from django.urls import path
from .views import OwnerUpdateView, OwnerLIstCreateView, OwnerNumberCheckView

urlpatterns = [
    path('', OwnerLIstCreateView.as_view(),),
    path('update/', OwnerUpdateView.as_view()),

    # 사업자 번호 확인 요청 URL
    path('business_license/check/', OwnerNumberCheckView.as_view()),
]
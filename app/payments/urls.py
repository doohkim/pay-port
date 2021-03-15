from django.urls import path

from payments.views import PaymentListAPIView, PaymentCreateAPIView

urlpatterns = [
    path('request/list/', PaymentListAPIView.as_view()),
    path('request/create/', PaymentCreateAPIView.as_view()),
    # 결제 부분은 업데이트 없는것으로
    # 비지니스 프로세스가 취소 -> 다시 결제
    path('request/update/', PaymentCreateAPIView.as_view()),

]

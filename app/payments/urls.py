from django.urls import path

from payments.views import PaymentListAPIView, PaymentCreateAPIView

urlpatterns = [
    path('request/list/', PaymentListAPIView.as_view()),
    path('request/create/', PaymentCreateAPIView.as_view()),
]
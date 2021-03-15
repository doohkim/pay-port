from django.urls import path

from paymethod.views import SettlementInformationListCreateAPIVew, SettlementInformationUpdate, \
    PaymentMethodCreateAPIView, PaymentMethodListAPIView, PaymentMethodUpdateAPIView

urlpatterns = [
    # list / create 같은 url
    path('', SettlementInformationListCreateAPIVew.as_view()),
    path('update/', SettlementInformationUpdate.as_view()),

    path('method/', PaymentMethodListAPIView.as_view()),
    path('method/create/', PaymentMethodCreateAPIView.as_view()),
    path('method/update/', PaymentMethodUpdateAPIView.as_view()),
]

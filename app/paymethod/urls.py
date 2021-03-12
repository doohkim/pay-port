from django.urls import path

from paymethod.views import SettlementInformationListCreateAPIVew, SettlementInformationUpdate, #PaymentMethodCreateAPIView

urlpatterns = [
    path('', SettlementInformationListCreateAPIVew.as_view()),
    path('update/', SettlementInformationUpdate.as_view()),

    # path('method/create/', PaymentMethodCreateAPIView.as_view()),
]
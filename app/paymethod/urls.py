from django.urls import path

from paymethod.views import SettlementInformationListCreateAPIVew, PaymentMethodCreateAPIView, PaymentMethodListAPIView, \
    PaymentMethodUpdateAPIView, PaymentMethodRetrieveAPIView, SettlementInformationUpdateAPIView, \
    SettlementInformationRetrieveAPIView

urlpatterns = [
    # list / create 같은 url
    path('settlement/', SettlementInformationListCreateAPIVew.as_view()),
    path('settlement/update/', SettlementInformationUpdateAPIView.as_view()),
    path('settlement/retrieve/', SettlementInformationRetrieveAPIView.as_view()),

    path('method/', PaymentMethodListAPIView.as_view()),
    path('method/create/', PaymentMethodCreateAPIView.as_view()),
    path('method/update/', PaymentMethodUpdateAPIView.as_view()),
    path('method/retrieve/', PaymentMethodRetrieveAPIView.as_view()),
]

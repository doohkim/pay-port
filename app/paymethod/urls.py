from django.urls import path

from paymethod.views import SettlementInformationListCreateAPIVew, PaymentMethodCreateAPIView, PaymentMethodListAPIView, \
    PaymentMethodUpdateAPIView, PaymentMethodRetrieveAPIView, SettlementInformationUpdateAPIView, \
    SettlementInformationRetrieveAPIView, SettlementAccountListAPIView, SettlementAccountCreateAPIView, \
    PaymentMethodSettlementCycleListAPIView, PaymentMethodSettlementCycleCreateAPIView\
    #, SettlementInformationListAPIVew

urlpatterns = [
    # 정산정보 API
    # list / create 같은 url
    path('settlement/create/', SettlementInformationListCreateAPIVew.as_view()),
    # path('settlement/', SettlementInformationListAPIVew.as_view()),
    path('settlement/update/', SettlementInformationUpdateAPIView.as_view()),
    path('settlement/retrieve/', SettlementInformationRetrieveAPIView.as_view()),

    # 정산계좌 API
    path('settlement/account/', SettlementAccountListAPIView.as_view()),
    path('settlement/account/create/', SettlementAccountCreateAPIView.as_view()),

    # 결제서비스 정보 API
    path('method/', PaymentMethodListAPIView.as_view()),
    path('method/create/', PaymentMethodCreateAPIView.as_view()),
    path('method/update/', PaymentMethodUpdateAPIView.as_view()),
    path('method/retrieve/', PaymentMethodRetrieveAPIView.as_view()),

    # 결제서비스 정산 주기 API
    path('method/cycle/', PaymentMethodSettlementCycleListAPIView.as_view()),
    path('method/cycle/create/', PaymentMethodSettlementCycleCreateAPIView.as_view()),
]

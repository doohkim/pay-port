from django.urls import path

from paymethod.views import SettlementInformationListCreateAPIVew, SettlementInformationUpdate

urlpatterns = [
    path('', SettlementInformationListCreateAPIVew.as_view()),
    path('update/', SettlementInformationUpdate.as_view()),

]
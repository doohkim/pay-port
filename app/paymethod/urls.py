from django.urls import path

from paymethod.views import SettlementInformationListCreateAPIVew

urlpatterns = [
    path('', SettlementInformationListCreateAPIVew.as_view()),

]
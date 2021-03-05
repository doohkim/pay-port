from django.urls import path
from .views import OwnerUpdateView, OwnerLIstCreateView

urlpatterns = [
    path('', OwnerLIstCreateView.as_view(),),
    path('update/', OwnerUpdateView.as_view())
]
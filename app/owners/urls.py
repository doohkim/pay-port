from django.urls import path
from .views import OwnerListAPIView, OwnerCreateView

urlpatterns = [
    path('list/', OwnerListAPIView.as_view(), name='owner-list'),
    path('create/', OwnerCreateView.as_view(),)
]
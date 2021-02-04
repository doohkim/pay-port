from django.urls import path
from .views import OwnerListCreateAPIView, OwnerCreateView

urlpatterns = [
    path('list/', OwnerListCreateAPIView.as_view(), name='owner-list'),
    path('create/', OwnerCreateView.as_view(),)
]
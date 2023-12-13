from django.urls import path
from .views import (CreateCustomerAPIView)

urlpatterns = [
      path('create-customer/',CreateCustomerAPIView.as_view(), name='create-customer'),
]

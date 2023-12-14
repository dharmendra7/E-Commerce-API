from django.urls import path
from .views import (CreateCustomerAPIView,
                    ListCustomersAPIView,
                    UpdateCustomerAPIView,
                    CreateProductAPIView,
                    ListProductsAPIView,
                    CreateOrderAPIView,
                    ListOrderAPIView,
                    EditOrderAPIView,
                    GetOrderByProductNameAPIView,
                    GetOrderByCustomerNameAPIView)

urlpatterns = [
      path('create-customer/',CreateCustomerAPIView.as_view(), name='create-customer'),
      path('get-customers/',ListCustomersAPIView.as_view(), name='get-customers'),
      path('update-customer/<int:id>/',UpdateCustomerAPIView.as_view(), name='update-customers'),
      path('create-product/',CreateProductAPIView.as_view(), name='create-product'),
      path('get-products/',ListProductsAPIView.as_view(), name='get-products'),
      path('create-order/',CreateOrderAPIView.as_view(), name='create-order'),
      path('get-orders/',ListOrderAPIView.as_view(), name='get-orders'),
      path('update-order/<int:id>/',EditOrderAPIView.as_view(), name='update-order'),
      path('get-orders-by-name/',GetOrderByProductNameAPIView.as_view(), name='get-order-by-name'),
      path('get-orders-by-customer-name/',GetOrderByCustomerNameAPIView.as_view(), name='get-order-by-customer-name'),
]

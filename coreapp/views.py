from django.shortcuts import render
from rest_framework import generics
from .serializers import (CreateCustomerSerializer,
                          UpdateCustomerSerializer,
                          CreateProductSerializer,
                          CreateOrderSerializer,
                          EditOrderSerializer)
from .common import *
from .models import (User, 
                     Product, 
                     Order, 
                     OrderItem)

# Create your views here.

class CreateCustomerAPIView(generics.GenericAPIView):
    serializer_class = CreateCustomerSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return send_response_validation(request, code=200, message=("Customer created successfully"))
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return send_response_validation(request, code=400, message=(error_msg_value[0]))
        except Exception as e:
            return error_400(request, message=str(e))
        
    
class ListCustomersAPIView(generics.GenericAPIView):
    def get(self, request):
        try:
            customers = User.objects.all()
            respone = [{
                "customer_id" : value.id,
                "name": value.name,
                "contact_number" : value.contact_number,
            }for value in customers]
            return JsonResponse(respone, safe=False)
        except Exception as e:
            return error_400(request, message=str(e))
        

class UpdateCustomerAPIView(generics.GenericAPIView):
    serializer_class = UpdateCustomerSerializer

    def put(self, request, id):
        try:
            serializer = self.serializer_class(data=request.data,context={'customer_id': id})
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return JsonResponse({
                        "message" : "Customer data is edited succesfully"
                })
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))
        except Exception as e:
            return error_400(request, message=str(e))


class CreateProductAPIView(generics.GenericAPIView):
    serializer_class = CreateProductSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return send_response_validation(request, code=200, message=("Product created successfully"))
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))        
        except Exception as e:
            return error_400(request, message=str(e))


class ListProductsAPIView(generics.GenericAPIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            respone = [{
                "product_id" : value.id,
                "name": value.name,
                "weight" : value.weight,
            }for value in products]
            return JsonResponse(respone, safe=False)
        except Exception as e:
            return error_400(request, message=str(e))
        

class CreateOrderAPIView(generics.GenericAPIView):
    serializer_class = CreateOrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return send_response_validation(request, code=200, message=("Order created successfully"))
        else:
            error_msg_value = list(serializer.errors.values())[0]
            return error_400(request,message=(error_msg_value[0]))  


class ListOrderAPIView(generics.GenericAPIView):
    def get(self, request):
        try:
            orders = Order.objects.all()
            respone = [{
                "customer_id" : value.customer.name,
                "order_id": value.order_number,
                "order_date" : value.order_date,
                "address" : value.address,
                "order_item" : [{ 
                    "product_name" : item.product.name, 
                    "quantity":item.quantity 
                }for item in OrderItem.objects.filter(order=value.id)]
            }for value in orders]
            return JsonResponse(respone, safe=False)
        except Exception as e:
            return error_400(request, message=str(e))
        

class EditOrderAPIView(generics.GenericAPIView):
    serializer_class = EditOrderSerializer

    def put(self, request, id):
        serializer = self.serializer_class(data=request.data, context = {'order_id': id})
        if serializer.is_valid():
            serializer.save()
            return send_response_validation(request, code=200, message=("Order edited successfully"))
        else:
            error_msg_value = list(serializer.errors.values())[0]
            return error_400(request,message=(error_msg_value[0]))


class GetOrderByProductNameAPIView(generics.GenericAPIView):
    def get_queryset(self):
        products = self.request.GET.get('products', '')
        product_names = products.split(',')
        if products:
            return Order.objects.filter(orderitem__product__name__in=product_names).distinct()
        else:
            return False
        
    def get(self, request):
        queryset = self.get_queryset()
        if queryset is not False:
            respone = [{
                "customer_id" : value.customer.name,
                "order_id": value.order_number,
                "order_date" : value.order_date,
                "address" : value.address,
                "order_item" : [{ 
                    "product_name" : item.product.name, 
                    "quantity":item.quantity 
                }for item in OrderItem.objects.filter(order=value.id)]
            }for value in queryset]
            return JsonResponse(respone, safe=False)
        else:
            return error_400(request, message='products are required')
        

class GetOrderByCustomerNameAPIView(generics.GenericAPIView):
    def get_queryset(self):
        customer_name = self.request.GET.get('customer', '')
        if customer_name:
            return Order.objects.filter(customer__name=customer_name).distinct()
        else:
            return False
        
    def get(self, request):
        queryset = self.get_queryset()
        if queryset is not False:
            respone = [{
                "customer_id" : value.customer.name,
                "order_id": value.order_number,
                "order_date" : value.order_date,
                "address" : value.address,
                "order_item" : [{ 
                    "product_name" : item.product.name, 
                    "quantity":item.quantity 
                }for item in OrderItem.objects.filter(order=value.id)]
            }for value in queryset]
            return JsonResponse(respone, safe=False)
        else:
            return error_400(request, message='customer name is required')
from django.shortcuts import render
from rest_framework import generics
from .serializers import (CreateCustomerSerializer)
from .common import *

# Create your views here.

class CreateCustomerAPIView(generics.GenericAPIView):
    serializer_class = CreateCustomerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return send_response_validation(request, code=200, message=("Customer created successfully"))
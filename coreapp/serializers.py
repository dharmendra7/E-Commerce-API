from rest_framework import serializers
from .models import (User)

import re

class CreateCustomerSerializer(serializers.Serializer):
    name = serializers.CharField()
    contact_number = serializers.CharField()
    email = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super(CreateCustomerSerializer, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages['blank'] = u'name field cannot be blank'
        self.fields['name'].error_messages['required'] = u'name field is required'
        self.fields['contact_number'].error_messages['blank'] = u'contact_number field cannot be blank'
        self.fields['contact_number'].error_messages['required'] = u'contact_number field is required'
        self.fields['email'].error_messages['blank'] = u'email field cannot be blank'
        self.fields['email'].error_messages['required'] = u'email field is required'

    def validate(self, attrs):
        email = attrs.get('email', '')
        contact_number = attrs.get('contact_number', '')
        name = attrs.get('name', '')

        if User.objects.filter(name=name).exists():
            raise serializers.ValidationError("Name already in use")

        if User.objects.filter(contact_number=contact_number).exists():
            raise serializers.ValidationError("Contact number already in use")
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already in use")

        return attrs
    
    def create(self, validatecurrent_seasond_data):
        user = User.objects.create_user(**validatecurrent_seasond_data)
        return user
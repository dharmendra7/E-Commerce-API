from rest_framework import serializers
from rest_framework.fields import empty
from .models import (User, 
                     Product, 
                     Order, 
                     OrderItem)

from datetime import date

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
            raise serializers.ValidationError('Name already in use')

        if User.objects.filter(contact_number=contact_number).exists():
            raise serializers.ValidationError('Contact number already in use')
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already in use')

        return attrs
    
    def create(self, validatecurrent_seasond_data):
        user = User.objects.create(**validatecurrent_seasond_data)
        return user
    

class UpdateCustomerSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    contact_number = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    # def __init__(self, *args, **kwargs):
    #     super(UpdateCustomerSerializer, self).__init__(*args, **kwargs)
    #     self.fields['customer_id'].error_messages['blank'] = u'customer_id field cannot be blank'
    #     self.fields['customer_id'].error_messages['required'] = u'customer_id field is required'

    def validate(self, attrs):
        if not User.objects.filter(id = self.context.get('customer_id')).exists():
            raise serializers.ValidationError('Customer does not exists.')
        
        if attrs.get('name') or attrs.get('contact_number') or attrs.get('email'):
            if attrs.get('name'):
                if User.objects.filter(name=attrs.get('name')).exists():
                    raise serializers.ValidationError('Name already in use')
            
            if attrs.get('contact_number'):
                if User.objects.filter(contact_number=attrs.get('contact_number')).exists():
                    raise serializers.ValidationError('Contact number already in use')
            
            if attrs.get('email'):
                if User.objects.filter(email=attrs.get('email')).exists():
                    raise serializers.ValidationError('Email already in use')
        else:
            raise serializers.ValidationError('Atleast one field is requierd')
        
        return attrs
    
    def create(self, validated_data):
        User.objects.filter(id = self.context.get('customer_id')).update(**validated_data)
        return True
    

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CreateProductSerializer, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages['blank'] = u'name field cannot be blank'
        self.fields['name'].error_messages['required'] = u'name field is required'
        self.fields['weight'].error_messages['blank'] = u'weight field cannot be blank'
        self.fields['weight'].error_messages['required'] = u'weight field is required'

    def validate(self, attrs):
        if attrs.get('weight')<0 or attrs.get('weight') > 25:
            raise serializers.ValidationError('Weight must be a positive decimal and not more than 25kg.')
        return attrs
    

class NestedProductsSerilazer(serializers.Serializer):
    product = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False)

class CreateOrderSerializer(serializers.Serializer):
    customer = serializers.IntegerField()
    order_date = serializers.DateField()
    address = serializers.CharField()
    order_item = NestedProductsSerilazer(many=True)

    def __init__(self, *args, **kwargs):
        super(CreateOrderSerializer, self).__init__(*args, **kwargs)
        self.fields['customer'].error_messages['blank'] = u'customer field cannot be blank'
        self.fields['customer'].error_messages['required'] = u'customer field is required'
        self.fields['order_date'].error_messages['blank'] = u'order_date field cannot be blank'
        self.fields['order_date'].error_messages['required'] = u'order_date field is required'
        self.fields['address'].error_messages['blank'] = u'address field cannot be blank'
        self.fields['address'].error_messages['required'] = u'address field is required'
        self.fields['order_item'].error_messages['blank'] = u'order_item field cannot be blank'
        self.fields['order_item'].error_messages['required'] = u'order_item field is required'

    def validate_order_date(self, value):
        if value < date.today():
            raise serializers.ValidationError('Order date cannot be in the past.')
        return value

    def validate(self, data):
        if not User.objects.filter(id = data.get('customer')).exists():
            raise serializers.ValidationError('Customer does not exists.')
        for item in data['order_item']:
            if item.get('product'):
                if not Product.objects.filter(id = item.get('product')).exists():
                    raise serializers.ValidationError("product does not exists")
            else:
                raise serializers.ValidationError('product is required')
            
            if item.get('quantity'):
                if item.get('quantity') < 0:
                    raise serializers.ValidationError('quntity must be a positive number')
            else:
                raise serializers.ValidationError('quantity is required')
        return data

    def create(self, validated_data):
        customer = validated_data.pop('customer')
        order_item = validated_data.pop('order_item')
        order_instance = Order.objects.create(customer = User.objects.get(id = customer),
                             **validated_data)
        for item in order_item:
            OrderItem.objects.create(order = order_instance, 
                                     product = Product.objects.get(id=item.pop('product')),
                                     **item)
        return validated_data


class EditOrderSerializer(serializers.Serializer):
    # customer = serializers.IntegerField(required=False)
    order_date = serializers.DateField(required=False)
    address = serializers.CharField(required=False)
    order_item = NestedProductsSerilazer(many=True)

    def validate(self, data):
        if not Order.objects.filter(id = self.context.get('order_id')).exists():
            raise serializers.ValidationError('Order does not exists.')

        if data.get('customer'):
            if not User.objects.filter(id = data.get('customer')).exists():
                raise serializers.ValidationError('Customer does not exists.')
            
        if data.get('order_date'):
            if data.get('order_date') < date.today():
                raise serializers.ValidationError('Order date cannot be in the past.')
            
        if data['order_item']:
            for item in data['order_item']:
                if item.get('product'):
                    if not Product.objects.filter(id = item.get('product')).exists():
                        raise serializers.ValidationError("product does not exists")
                else:
                    raise serializers.ValidationError('product is required')
                
                if item.get('quantity'):
                    if item.get('quantity') < 0:
                        raise serializers.ValidationError('quntity must be a positive number')
                else:
                    raise serializers.ValidationError('quantity is required')
        return data

    def create(self, validated_data):
        order_item = validated_data.pop('order_item')
        order_instance = Order.objects.filter(id = self.context.get("order_id")).update(**validated_data)
        for item in order_item:
            OrderItem.objects.update_or_create( order = Order.objects.get(id = self.context.get("order_id")),
                                     product = Product.objects.get(id=item.pop('product')),
                                     **item)
        return validated_data


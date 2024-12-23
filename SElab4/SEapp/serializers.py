from rest_framework import serializers
from .models import Product, Customer, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("At least one field is required for update.")
        return data

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'address']

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'products', 'date', 'status', 'total_order_price']
        read_only_fields = ['total_order_price']
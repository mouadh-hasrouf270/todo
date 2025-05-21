from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Client, MenuItem, MenuList, Restaurant, Delivery, Order, OrderItem

class SingUpSerializers(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'last_name', 'email', 'password', 'role')
        extra_kwargs = {
            'username': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'role': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    
    class Meta:
        model = Client
        fields = ['client_id', 'user', 'user_id', 'name', 'address', 'phone_number', 'email']
        read_only_fields = ['client_id']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image', 'is_available']
        read_only_fields = ['id']

class MenuListSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = MenuList
        fields = ['id', 'name', 'items']
        read_only_fields = ['id']

class RestaurantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    menu_list = MenuListSerializer(read_only=True)
    
    class Meta:
        model = Restaurant
        fields = ['restaurant_id', 'user', 'user_id', 'name', 'address', 'phone_number', 'email', 'is_available', 'menu_list']
        read_only_fields = ['restaurant_id']

class DeliverySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    
    class Meta:
        model = Delivery
        fields = ['delivery_id', 'user', 'user_id', 'name', 'phone_number', 'email', 'working_zone', 'is_available', 'vehicle_type', 'current_order']
        read_only_fields = ['delivery_id', 'current_order']

class OrderItemSerializer(serializers.ModelSerializer):
    item = MenuItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        source='item',
        write_only=True
    )
    
    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'item_id', 'quantity', 'price']
        read_only_fields = ['id', 'price']

class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    delivery = DeliverySerializer(read_only=True)
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['order_id', 'client', 'restaurant', 'delivery', 'items', 'status', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['order_id', 'total_price', 'created_at', 'updated_at']


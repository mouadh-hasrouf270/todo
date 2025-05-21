from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Client, MenuItem, MenuList, Restaurant, Delivery, Order, OrderItem

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_superuser')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'name', 'email', 'phone_number')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('user__is_active',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'is_available')
    search_fields = ('name', 'description')
    list_filter = ('is_available',)

@admin.register(MenuList)
class MenuListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    filter_horizontal = ('items',)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant_id', 'name', 'email', 'phone_number', 'is_available')
    search_fields = ('name', 'email', 'phone_number', 'address')
    list_filter = ('is_available',)

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_id', 'name', 'email', 'phone_number', 'is_available', 'vehicle_type')
    search_fields = ('name', 'email', 'phone_number', 'working_zone')
    list_filter = ('is_available', 'vehicle_type')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'client', 'restaurant', 'delivery', 'status', 'total_price', 'created_at')
    search_fields = ('order_id', 'client__name', 'restaurant__name', 'delivery__name')
    list_filter = ('status', 'created_at')
    date_hierarchy = 'created_at'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'item', 'quantity', 'price')
    search_fields = ('order__order_id', 'item__name')
    list_filter = ('order__status',)

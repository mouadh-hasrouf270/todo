from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('delivery', 'Delivery Worker'),
        ('restaurant', 'Restaurant'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')

    def __str__(self):
        return f"{self.username} - {self.role}"
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    client_id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return f"{self.name} - {self.client_id}"
    
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='menu_items', null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
class MenuList(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(MenuItem)
    
    def __str__(self):
        return self.name
    
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    restaurant_id = models.AutoField(primary_key=True)
    is_available = models.BooleanField(default=True)
    menu_list = models.ForeignKey(MenuList, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.restaurant_id}"

class Delivery(models.Model):
    VEHICLE_CHOICES = (
        ('bike', 'Bike'),
        ('motorcycle', 'Motorcycle'),
        ('car', 'Car'),
        ('van', 'Van'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    delivery_id = models.AutoField(primary_key=True)
    working_zone = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    current_order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_delivery')
    
    def __str__(self):
        return f"{self.name} - {self.delivery_id}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('ready', 'Ready for Pickup'),
        ('delivered', 'Delivered'),
    )
    
    order_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.item.name} in Order {self.order.order_id}"



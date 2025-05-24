from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate,logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import SingUpSerializers, ClientSerializer, RestaurantSerializer, DeliverySerializer, MenuItemSerializer,OrderSerializer,OrderItemSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Restaurant, Delivery, MenuItem,MenuList,Order,OrderItem
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as auth_login
from django.db.models import Q
from decimal import Decimal
from django.db import transaction
from django.core.mail import send_mail
from notifications.models import Notification


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_users(request):
    request.user.auth_token.delete()
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def client_signup(request):
    User = get_user_model()
    data = request.data
    
    # Check if user already exists
    if User.objects.filter(email=data.get('email')).exists():
        return Response(
            {'error': 'This email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user account
    user_data = {
        'username': data.get('username'),
        'last_name': data.get('last_name'),
        'email': data.get('email'),
        'role': 'client',
        'password': data.get('password'),
    }
    
    user_serializer = SingUpSerializers(data=user_data)
    if user_serializer.is_valid():
        user = User.objects.create(
            username=user_data['username'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            role=user_data['role'],
            password=make_password(user_data['password']),
        )
        
        # Create client profile
        client_data = {
            'user_id': user.id,
            'name': data.get('name'),
            'address': data.get('address'),
            'phone_number': data.get('phone_number'),
            'email': data.get('email'),
        }
        send_mail(
                subject='Welcome to Our Delivery Platform',
                message='Hello, your client account has been created successfully!',
                from_email=None,  # use DEFAULT_FROM_EMAIL
                recipient_list=[user.email],
                fail_silently=False,
            )
        
        client_serializer = ClientSerializer(data=client_data)
        if client_serializer.is_valid():
            client_serializer.save()
            return Response({
                'detail': 'Client account registered successfully',
                'client': client_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            # If client creation fails, delete the user
            user.delete()
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def restaurant_signup(request):
    User = get_user_model()
    data = request.data
    
    # Check if user already exists
    if User.objects.filter(email=data.get('email')).exists():
        return Response(
            {'error': 'This email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user account
    user_data = {
        'username': data.get('username'),
        'last_name': data.get('last_name'),
        'email': data.get('email'),
        'role': 'restaurant',
        'password': data.get('password'),
    }
    
    user_serializer = SingUpSerializers(data=user_data)
    if user_serializer.is_valid():
        user = User.objects.create(
            username=user_data['username'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            role=user_data['role'],
            password=make_password(user_data['password']),
        )
        
        # Create restaurant profile
        restaurant_data = {
            'user_id': user.id,
            'name': data.get('name'),
            'address': data.get('address'),
            'phone_number': data.get('phone_number'),
            'email': data.get('email'),
            'is_available': True,
        }
        send_mail(
                subject='Welcome to Our Delivery Platform',
                message='Hello, your restaurant account has been created successfully!',
                from_email=None,  # use DEFAULT_FROM_EMAIL
                recipient_list=[user.email],
                fail_silently=False,
            )
        
        restaurant_serializer = RestaurantSerializer(data=restaurant_data)
        if restaurant_serializer.is_valid():
            restaurant_serializer.save()
            return Response({
                'detail': 'Restaurant account registered successfully',
                'restaurant': restaurant_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            # If restaurant creation fails, delete the user
            user.delete()
            return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def delivery_signup(request):
    User = get_user_model()
    data = request.data
    
    # Check if user already exists
    if User.objects.filter(email=data.get('email')).exists():
        return Response(
            {'error': 'This email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user account
    user_data = {
        'username': data.get('username'),
        'last_name': data.get('last_name'),
        'email': data.get('email'),
        'role': 'delivery',
        'password': data.get('password'),
    }
    
    user_serializer = SingUpSerializers(data=user_data)
    if user_serializer.is_valid():
        user = User.objects.create(
            username=user_data['username'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            role=user_data['role'],
            password=make_password(user_data['password']),
        )
        
        # Create delivery profile
        delivery_data = {
            'user_id': user.id,
            'name': data.get('name'),
            'phone_number': data.get('phone_number'),
            'email': data.get('email'),
            'working_zone': data.get('working_zone'),
            'is_available': True,
            'vehicle_type': data.get('vehicle_type'),
        }
        send_mail(
                subject='Welcome to Our Delivery Platform',
                message='Hello, your delivery account has been created successfully!',
                from_email=None,  # use DEFAULT_FROM_EMAIL
                recipient_list=[user.email],
                fail_silently=False,
            )
        
        delivery_serializer = DeliverySerializer(data=delivery_data)
        if delivery_serializer.is_valid():
            delivery_serializer.save()
            return Response({
                'detail': 'Delivery account registered successfully',
                'delivery': delivery_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            # If delivery creation fails, delete the user
            user.delete()
            return Response(delivery_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Please provide both email and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get the user by email
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Check if the password is correct
    if not user.check_password(password):
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Create or get token
    token, created = Token.objects.get_or_create(user=user)
    
    # Get user profile based on role
    profile_data = {}
    if user.role == 'client':
        try:
            client = Client.objects.get(user=user)
            profile_data = ClientSerializer(client).data
        except Client.DoesNotExist:
            pass
    elif user.role == 'restaurant':
        try:
            restaurant = Restaurant.objects.get(user=user)
            profile_data = RestaurantSerializer(restaurant).data
        except Restaurant.DoesNotExist:
            pass
    elif user.role == 'delivery':
        try:
            delivery = Delivery.objects.get(user=user)
            profile_data = DeliverySerializer(delivery).data
        except Delivery.DoesNotExist:
            pass
    
    # Return user data and token
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
        },
        'profile': profile_data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_restaurants(request):
    """
    Search restaurants by name, address, or other criteria.
    Only authenticated users can search restaurants.
    """
    # Get search parameters from query string
    search_query = request.GET.get('q', '')
    address = request.GET.get('address', '')
    
    # Start with all restaurants
    restaurants = Restaurant.objects.filter(is_available=True)
    
    # Apply search filters if provided
    if search_query:
        restaurants = restaurants.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if address:
        restaurants = restaurants.filter(address__icontains=address)
    
    # Serialize the results
    serializer = RestaurantSerializer(restaurants, many=True)
    
    return Response({
        'count': restaurants.count(),
        'results': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_restaurant_menu(request, restaurant_id):
    """
    Get all menu items for a specific restaurant.
    Only authenticated users can access this endpoint.
    """
    try:
        restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {'error': f'Restaurant with ID {restaurant_id} does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if not restaurant.is_available:
        return Response(
            {'error': f'Restaurant {restaurant.name} is not currently available'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if not restaurant.menu_list:
        return Response(
            {
                'error': f'Restaurant {restaurant.name} has no menu items',
                'restaurant_info': {
                    'id': restaurant.restaurant_id,
                    'name': restaurant.name,
                    'address': restaurant.address,
                    'phone': restaurant.phone_number
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get all menu items from the restaurant's menu list
    menu_items = restaurant.menu_list.items.all()
    
    if not menu_items.exists():
        return Response(
            {
                'error': f'Restaurant {restaurant.name} has no available menu items',
                'restaurant_info': {
                    'id': restaurant.restaurant_id,
                    'name': restaurant.name,
                    'address': restaurant.address,
                    'phone': restaurant.phone_number
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = MenuItemSerializer(menu_items, many=True)
    
    return Response({
        'restaurant_info': {
            'id': restaurant.restaurant_id,
            'name': restaurant.name,
            'address': restaurant.address,
            'phone': restaurant.phone_number
        },
        'menu_items': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def add_menu_item(request):
    user = request.user
    if user.role != 'restaurant':
        return Response({'error': 'Only restaurants can add menu items.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        restaurant = Restaurant.objects.get(user=user)
    except Restaurant.DoesNotExist:
        return Response({'error': 'Restaurant not found.'}, status=status.HTTP_404_NOT_FOUND)

    menu_list = restaurant.menu_list
    if not menu_list:
        menu_list = MenuList.objects.create(name=f"{restaurant.user.full_name} menu")
        restaurant.menu_list = menu_list
        restaurant.save()

    data = request.data.copy()
    data['menu_list'] = menu_list.id  # Assign menu_list ID directly

    serializer = MenuItemSerializer(data=data)
    if serializer.is_valid():
        menu_item = serializer.save()
        menu_list.items.add(menu_item)  # Ensure it's added to the chosen items
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_menu_item(request, item_id):
    """
    Update an existing menu item.
    Only authenticated restaurant users who own the item can update it.
    """
    # Check if the authenticated user is a restaurant
    user = request.user
    if user.role != 'restaurant':
        return Response(
            {'error': 'Only restaurant accounts can update menu items'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get the restaurant profile
    try:
        restaurant = Restaurant.objects.get(user=user)
    except Restaurant.DoesNotExist:
        return Response(
            {'error': 'Restaurant profile not found for this user'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Find the menu item
    try:
        menu_item = MenuItem.objects.get(id=item_id)
    except MenuItem.DoesNotExist:
        return Response(
            {'error': f'Menu item with ID {item_id} does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Update the menu item
    serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'detail': 'Menu item updated successfully',
            'menu_item': serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_menu_item(request, item_id):
    """
    Delete a menu item.
    Only authenticated restaurant users who own the item can delete it.
    """
    # Check if the authenticated user is a restaurant
    user = request.user
    if user.role != 'restaurant':
        return Response(
            {'error': 'Only restaurant accounts can delete menu items'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get the restaurant profile
    try:
        restaurant = Restaurant.objects.get(user=user)
    except Restaurant.DoesNotExist:
        return Response(
            {'error': 'Restaurant profile not found for this user'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Find the menu item
    try:
        menu_item = MenuItem.objects.get(id=item_id)
    except MenuItem.DoesNotExist:
        return Response(
            {'error': f'Menu item with ID {item_id} does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    
    # Delete the menu item
    menu_item.delete()
    
    return Response({
        'detail': 'Menu item deleted successfully'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def show_restaurant(request,item_id):
    restaurants = Restaurant.objects.get(restaurant_id=item_id)
    serializer = RestaurantSerializer(restaurants)
    return Response(serializer.data)
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def add_order(request):
    user = request.user
    if user.role != 'client':
        return Response({'error': 'Only clients can place orders.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        client = Client.objects.get(user=user)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        restaurant_user = request.data.get('restaurant_id')
        restaurant = Restaurant.objects.get(restaurant_id=restaurant_user)
    except Restaurant.DoesNotExist:
        return Response({'error': 'Restaurant not found.'}, status=status.HTTP_404_NOT_FOUND)

    items_data = request.data.get('items')
    if not items_data or not isinstance(items_data, list):
        return Response({'error': 'Items must be a list of objects with item_id and quantity.'}, status=status.HTTP_400_BAD_REQUEST)

    total_price = 0
    order_items = []

    # Validate items first
    for entry in items_data:
        item_id = entry.get('item_id')
        quantity = int(entry.get('quantity', 1))
        try:
            item = MenuItem.objects.get(id=item_id)
            total_price += item.price * quantity
            order_items.append((item, quantity))
        except MenuItem.DoesNotExist:
            return Response({'error': f'Menu item with id {item_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Create order
    order = Order.objects.create(
        client=client,
        restaurant=restaurant,
        total_price=total_price,
        status='confirmed'
    )

    # Add order items
    for item, quantity in order_items:
        OrderItem.objects.create(
            order=order,
            item=item,
            quantity=quantity,
            price=item.price
        )

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def mark_order_ready(request, order_id):
    try:
        user = request.user
        restaurant = Restaurant.objects.get(user=user)
    except Restaurant.DoesNotExist:
        return Response({'error': 'Restaurant not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        order = Order.objects.get(order_id=order_id, restaurant=restaurant)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found or not associated with your restaurant.'}, status=status.HTTP_404_NOT_FOUND)

    if order.status != 'confirmed':
        return Response({'error': 'Only confirmed orders can be marked as ready.'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = 'ready'
    order.save()
    Notification.objects.create(
    user=order.client.user,
    message=f'Your order #{order.order_id} status changed to "{order.status}"'
)

    return Response({'message': f"Order {order.order_id} marked as ready."}, status=status.HTTP_200_OK)
@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def restaurant_orders(request):
    user = request.user
    if user.role != 'restaurant':
        return Response({'error': 'Only restaurants can view their orders.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        restaurant = Restaurant.objects.get(user=user)
    except Restaurant.DoesNotExist:
        return Response({'error': 'Restaurant not found.'}, status=status.HTTP_404_NOT_FOUND)

    orders = Order.objects.filter(restaurant=restaurant).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def ready_orders_for_delivery(request):
    user = request.user
    if user.role != 'delivery':
        return Response({'error': 'Only delivery personnel can view ready orders.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        delivery_person = Delivery.objects.get(user=user)
    except Delivery.DoesNotExist:
        return Response({'error': 'Delivery profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Get all orders with status "ready" and no delivery assigned yet
    ready_orders = Order.objects.filter(status='ready', delivery__isnull=True).order_by('-created_at')

    serializer = OrderSerializer(ready_orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def pickup_order(request, order_id):
    user = request.user
    if user.role != 'delivery':
        return Response({'error': 'Only delivery personnel can pick up orders.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        delivery_person = Delivery.objects.get(user=user)
    except Delivery.DoesNotExist:
        return Response({'error': 'Delivery profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    if order.status != 'ready':
        return Response({'error': 'Only ready orders can be picked up.'}, status=status.HTTP_400_BAD_REQUEST)

    if order.delivery is not None:
        return Response({'error': 'This order has already been assigned to a delivery person.'}, status=status.HTTP_400_BAD_REQUEST)

    # Assign delivery and mark as delivered
    order.delivery = delivery_person
    order.status = 'delivered'
    order.save()
    Notification.objects.create(
    user=order.client.user,
    message=f'Your order #{order.order_id} status changed to "{order.status}"'
)

    return Response({'message': f"Order {order.order_id} marked as delivered and assigned to you."}, status=status.HTTP_200_OK)
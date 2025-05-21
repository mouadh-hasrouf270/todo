from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import SingUpSerializers, ClientSerializer, RestaurantSerializer, DeliverySerializer, MenuItemSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Restaurant, Delivery, MenuItem
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as auth_login
from django.db.models import Q

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    User = get_user_model()
    data= request.data
    user=SingUpSerializers(data=data)
    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                username = data['username'],
                last_name=data['last_name'],
                email=data['email'],
                role=data['role'],
                password=make_password(data['password']),
            )
            return Response({'detail':'Your acount registred'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': 'this exail already exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(user.errors)

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
@permission_classes([IsAuthenticated])
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
    menu_items = restaurant.menu_list.items.filter(is_available=True)
    
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
    # Check if the authenticated user is a restaurant
    user = request.user
    
    # Debug information
    print(f"User: {user}, Type: {type(user)}, ID: {user.id}, Authenticated: {user.is_authenticated}")
    
    """if user.role != 'restaurant':
        return Response(
            {'error': 'Only restaurant accounts can add menu items'},
            status=status.HTTP_403_FORBIDDEN
        )"""
    
    # Get the restaurant profile - change how we query
    try:
        restaurant = Restaurant.objects.get(user_id=user.id)  # Use user_id explicitly
    except Restaurant.DoesNotExist:
        return Response(
            {'error': 'Restaurant profile not found for this user'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get data for the new menu item
    data = request.data.copy()  # Create a mutable copy
    
    # Check if restaurant has a menu_list
    if not hasattr(restaurant, 'menu_list') or restaurant.menu_list is None:
        return Response(
            {'error': 'Menu list not found for this restaurant'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Add restaurant's menu list reference to the data
    data['menu_list'] = restaurant.menu_list.id
    
    # Create the menu item
    serializer = MenuItemSerializer(data=data)
    if serializer.is_valid():
        menu_item = serializer.save()
        return Response({
            'detail': 'Menu item added successfully',
            'menu_item': serializer.data
        }, status=status.HTTP_201_CREATED)
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
    
    # Check if the menu item belongs to this restaurant
    if menu_item.menu_list != restaurant.menu_list:
        return Response(
            {'error': 'You do not have permission to update this menu item'},
            status=status.HTTP_403_FORBIDDEN
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
    
    # Check if the menu item belongs to this restaurant
    if menu_item.menu_list != restaurant.menu_list:
        return Response(
            {'error': 'You do not have permission to delete this menu item'},
            status=status.HTTP_403_FORBIDDEN
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
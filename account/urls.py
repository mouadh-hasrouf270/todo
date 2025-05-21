from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('client/signup/', views.client_signup, name='client_signup'),
    path('restaurant/signup/', views.restaurant_signup, name='restaurant_signup'),
    path('delivery/signup/', views.delivery_signup, name='delivery_signup'),
    path('login/', views.login, name='login'),
    path('restaurants/search/', views.search_restaurants, name='search_restaurants'),
    path('restaurants/<int:restaurant_id>/menu/', views.get_restaurant_menu, name='get_restaurant_menu'),
    path('menu/item/add/', views.add_menu_item, name='add-menu-item'),
    path('menu/item/<int:item_id>/update/', views.update_menu_item, name='update-menu-item'),
    path('menu/item/<int:item_id>/delete/', views.delete_menu_item, name='delete-menu-item'),
    path('restaurants/', views.restaurant_list, name='restaurant-list'),
    path('show_restaurants/<int:item_id>/', views.show_restaurant, name='show_restaurant'),
]

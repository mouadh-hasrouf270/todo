from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_users, name='logout'),
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
    path('addorder/', views.add_order, name='add_order'),
    path('orders/<int:order_id>/mark-ready/', views.mark_order_ready, name='mark_order_ready'),
    path('orders/restaurant/', views.restaurant_orders, name='restaurant_orders'),
    path('orders/delivery/', views.ready_orders_for_delivery, name='delivery_orders'),
    path('orders/<order_id>/pickup/', views.pickup_order, name='delivery_orders'),
    path('orders/delivery/history/', views.orders_for_delivery_person, name='delivery_orders_history'),
    path('orders/client/history/', views.orders_for_client_hestory, name='client_orders_history'),
    path('edit/client/', views.edit_client_profile, name='edit_client'),
    path('edit/restaurant/', views.edit_restaurant_profile, name='edit_restaurant'),
    path('edit/delivery/', views.edit_delivery_profile, name='edit_delivery'),
]

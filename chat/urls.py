from django.urls import path
from .views import room_api

urlpatterns = [
    path('api/room/<str:room_name>/', room_api),
]

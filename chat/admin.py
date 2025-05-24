from django.contrib import admin
from .models import PrivateRoom,Message

admin.site.register(Message)
admin.site.register(PrivateRoom)


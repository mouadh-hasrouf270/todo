from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PrivateRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_user2')

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"

class Message(models.Model):
    room = models.ForeignKey(PrivateRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Message
from .serializers import MessageSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def room_api(request, room_name):
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    messages = Message.objects.filter(room=room).order_by('timestamp')
    serialized_messages = MessageSerializer(messages, many=True)

    return Response({
        'room_name': room.name,
        'messages': serialized_messages.data
    })

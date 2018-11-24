from .serializers import *

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class ConversationView(APIView):

    def get(self, request, format=None):
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageView(APIView):

    def get(self, request, conversation_id, format=None):
        messages = Message.objects.filter(conversation_id=self.kwargs['conversation_id'])
        serializer = MessageSerializer(data=messages)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
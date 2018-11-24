from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ("id", "users")


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    conversation = ConversationSerializer()

    class Meta:
        model = Message
        fields = ("id", "user", "content", "conversation")

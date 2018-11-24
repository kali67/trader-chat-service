from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path(r"conversations/", ConversationView.as_view()),
    path(r"conversations/<int:conversation_id>/messages", MessageView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

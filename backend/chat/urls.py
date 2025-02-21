from django.urls import path

from chat.views import (
    ChatsView, MessagesView
)

urlpatterns = [
    path("", ChatsView.as_view(), name="chats"),
    path("<uuid:chat_id>/messages", MessagesView.as_view(), name="messages"),
]
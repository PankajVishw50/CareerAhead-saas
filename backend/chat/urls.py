from django.urls import path

from chat.views import (
    ChatsView, MessagesView,
    ChatView
)

urlpatterns = [
    path("", ChatsView.as_view(), name="chats"),
    path("<uuid:chat_id>", ChatView.as_view(), name="chat"),
    path("<uuid:chat_id>/messages", MessagesView.as_view(), name="messages"),
]

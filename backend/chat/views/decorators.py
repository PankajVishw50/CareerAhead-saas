
from chat.models import Chat
from util.response import ErrorResponseTemplates

def chat_exists(func):
    def wrapper(self, request, chat_id, *args, **kwargs):
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return ErrorResponseTemplates.NOT_FOUND("Chat not found")
        
        request.chat = chat
        return func(self, request, chat_id, *args, **kwargs)
    return wrapper

def user_owns_chat(func):
    def wrapper(self, request, chat_id, *args, **kwargs):
        if request.user != request.chat.user_a and request.user != request.chat.user_b:
            return ErrorResponseTemplates.FORBIDDEN("You are not allowed to access this resource")
        return func(self, request, chat_id, *args, **kwargs)
    return wrapper
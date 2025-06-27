from rest_framework.views import APIView, Response

from chat.serializers import ChatSerializer
from chat.views.decorators import chat_exists


class ChatView(APIView):
    @chat_exists
    def get(self, request, chat_id):
        return Response(ChatSerializer(request.chat).data)

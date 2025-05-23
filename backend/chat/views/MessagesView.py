from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django.core.paginator import Paginator, EmptyPage

from util.decorators import get_pagination_params, get_ordering_params
from util.helpers import paginated_response 
from chat.views.decorators import user_owns_chat
from util.response import ErrorResponseTemplates
from chat.views.decorators import chat_exists
from chat.models import Message, Chat
from chat.serializers import MessageSerializer
from util.decorators import get_pagination_params
from util.helpers import get_page_meta, paginated_response
from util.cursors import GeneralCursorPagination

class MessagesView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    @chat_exists
    @user_owns_chat
    def get(self, request, chat_id):

        query = request.chat.messages.all()
        paginator = GeneralCursorPagination() 
        try:
            page = paginator.paginate_queryset(query, request, self)
        except Exception:
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()
        
        messages_s = MessageSerializer(page, many=True)
        return Response({
            **paginator.get_html_context(),
            "items": messages_s.data,
        })
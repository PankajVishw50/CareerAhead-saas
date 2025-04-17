from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage

from util.decorators import get_pagination_params, get_ordering_params
from util.helpers import paginated_response 
from chat.views.decorators import user_owns_chat
from util.response import ErrorResponseTemplates
from chat.views.decorators import chat_exists
from chat.models import Message, Chat
from chat.serializers import MessageSerializer

class MessagesView(APIView):
    permission_classes = [IsAuthenticated]

    @get_pagination_params
    @get_ordering_params
    @chat_exists
    @user_owns_chat
    def get(self, request, chat_id):
        # import ipdb;ipdb.set_trace()

        query = request.chat.messages.all()
        if request.ordering == "asc":
            query = query.order_by("created_at")
        else:
            query = query.order_by("-created_at")

        paginator = Paginator(query, request.pagination.size)
        try:
            page = paginator.page(request.pagination.page)
        except EmptyPage:
            return ErrorResponseTemplates.PAGINATION_NOT_FOUND(paginator.num_pages)
        
        messages_s = MessageSerializer(page, many=True)
        return Response(page, messages_s.data)
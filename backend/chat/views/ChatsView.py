from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from util.response import ErrorResponseTemplates
from chat.models import Chat
from rest_framework.response import Response

from util.decorators import get_pagination_params, get_ordering_params
from chat.serializers import ChatSerializer
from util.helpers import paginated_response
from util.cursors import GeneralCursorPagination

class ChatsView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    
    @get_ordering_params
    @get_pagination_params
    def get(self, request):

        VALID_TYPES = ["available", "all", "disabled"]

        type_of = request.query_params.get("type", "available")

        match type_of:
            case "available":
                query = request.user.chats_valid()
            case "disabled":
                query = request.user.chats_invalid() 
            case "all":
                query = request.user.chats 
            case _:
                return ErrorResponseTemplates.BAD_REQUEST(
                    f"Invalid `type` value - should be one of these {VALID_TYPES}"
                )

        paginator = GeneralCursorPagination()
        try:
            # import ipdb;ipdb.set_trace()
            page = paginator.paginate_queryset(query, request, self)
        except Exception:
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()

        chats_s = ChatSerializer(page, many=True)
        return Response({
            **paginator.get_html_context(),
            "items": chats_s.data,
        })
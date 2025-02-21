from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from util.response import ErrorResponseTemplates
from chat.models import Chat
from rest_framework.response import Response

from util.decorators import get_pagination_params, get_ordering_params
from chat.serializers import ChatSerializer
from util.helpers import get_page_meta

class ChatsView(APIView):
    permission_classes = [IsAuthenticated]

    @get_ordering_params
    @get_pagination_params
    def get(self, request):

        VALID_TYPES = ["available", "all", "disabled"]
        VALID_ORDERS = ["asc", "desc"]

        type = request.data.get("type", "available")

        query = None
        match type:
            case "available":
                query = Chat.objects.all_valids()
            case "disabled":
                query = Chat.objects.all_invalids()
            case "all":
                query = Chat.objects.all()
            case _:
                return ErrorResponseTemplates.BAD_REQUEST(
                    f"Invalid `type` value - should be one of these {VALID_TYPES}"
                )
        match request.ordering:
            case "asc":
                query = query.order_by("modified_at")
            case "desc":
                query = query.order_by("-modified_at")
            case _:
                return ErrorResponseTemplates.BAD_REQUEST(
                    f"Invalid `order` value - should be one of these {VALID_ORDERS}"
                )
            
        paginator = Paginator(query, request.pagination.size)
        try:
            page = paginator.page(request.pagination.page)
        except EmptyPage:
            return ErrorResponseTemplates.PAGINATION_NOT_FOUND(paginator.num_pages)
        
        chats_s = ChatSerializer(page, many=True)
        return Response({
            "meta": get_page_meta(page),
            "items": chats_s.data,
        })

                

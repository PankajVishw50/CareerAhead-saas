import datetime
from django.db.models import Q
import pytz
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from counselling.models import CounsellingSession
from counselling.serializers import CounsellingSessionSerializer
from util.cursors import GeneralCursorPagination
from util.response import ErrorResponseTemplates


class SessionsView(APIView):
    permissions_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["from_datetime", "created_at"]
    ordering = ["-from_datetime"]

    def get(self, request):

        query = request.user.all_sessions.all()
        type_of = request.query_params.get("type", "all")
        now = datetime.datetime.now(pytz.utc)

        match type_of:
            case "active":
                query = query.filter(Q(from_datetime__lte=now) & Q(to_datetime__gt=now))
            case "upcoming":
                query = query.filter(Q(from_datetime__gt=now))
            case "old":
                query = query.filter(to_datetime__lte=now)
            case "all":
                query = query
            case _:
                return ErrorResponseTemplates.BAD_REQUEST(
                    f"Invalid `type` value - should be one of these {VALID_TYPES}"
                )

        paginator = GeneralCursorPagination()
        try:
            page = paginator.paginate_queryset(query, request, self)
        except Exception:
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()

        query_s = CounsellingSessionSerializer(page, many=True)
        return Response(
            {
                **paginator.get_html_context(),
                "items": query_s.data,
            }
        )

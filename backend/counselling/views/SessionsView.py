import datetime
from django.db.models import Q
import pytz
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import django_filters.rest_framework as filters
from counselling.filters import SessionsFiltler
from counselling.models import CounsellingSession
from counselling.serializers import CounsellingSessionSerializer
from util.cursors import GeneralCursorPagination
from util.response import ErrorResponseTemplates


class SessionsView(GenericAPIView):
    serializer_class = CounsellingSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = SessionsFiltler
    ordering_fields = ["from_datetime", "created_at"]
    ordering = ["-from_datetime"]

    def get_queryset(self):
        query = self.request.user.all_sessions.all()
        type_of = self.request.query_params.get("type", "all")
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

        return query

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        paginator = GeneralCursorPagination()
        try:
            page = paginator.paginate_queryset(queryset, request, self)
        except Exception:
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()

        serializer = CounsellingSessionSerializer(page, many=True)
        return Response(
            {
                **paginator.get_html_context(),
                "items": serializer.data,
            }
        )

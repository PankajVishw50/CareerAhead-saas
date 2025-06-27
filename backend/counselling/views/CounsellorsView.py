from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from counselling.models import Counsellor
from counselling.serializers import CounsellorSerializer
from counselling.filters import CounsellorModelFilterSet


class CounsellorsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Counsellor.objects.all()
    serializer_class = CounsellorSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]
    filterset_class = CounsellorModelFilterSet

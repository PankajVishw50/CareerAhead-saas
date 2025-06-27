from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import NotFound

from counselling.serializers import CounsellorSerializer
from counselling.views.decorators import counsellor_exists
from counselling.models import Counsellor
from util.response import ErrorResponseTemplates


class CounsellorView(APIView):
    permission_classes = [IsAuthenticated]

    @counsellor_exists
    def get(self, request, counsellor_id):
        counsellor_s = CounsellorSerializer(request.counsellor)
        return Response(counsellor_s.data)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from counselling.serializers import CounsellorSerializer
from counselling.views.decorators import counsellor_exists

class CounsellorView(APIView):
    permission_classes = [IsAuthenticated]

    @counsellor_exists
    def get(self, request, counsellor_id):
        serialized_data = CounsellorSerializer(request.counsellor)
        return Response(
            serialized_data.data,
        )

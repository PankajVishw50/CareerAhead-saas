from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.serializers import UserSerializer


class MeView(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        data = UserSerializer(request.user)
        return Response(data.data)

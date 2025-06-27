from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.serializers import UserSerializer
from util.models.shortcuts import User


class MeView(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request):
        # import ipdb;ipdb.set_trace()
        data = UserSerializer(request.user)
        return Response(data.data)

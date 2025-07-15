from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from account.serializers.UserSerializer import UserProfileSerializer
from util.models.shortcuts import User


class PublicUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

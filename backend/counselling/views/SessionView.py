from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from counselling.serializers import CounsellingSessionSerializer


class SessionView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CounsellingSessionSerializer

    def get_queryset(self):
        return self.request.user.all_sessions.all()

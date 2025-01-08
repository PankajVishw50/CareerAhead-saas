from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.signing import TimestampSigner


class SignedTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Create token
        t_signer = TimestampSigner()
        token = t_signer.sign(request.user.id)

        return Response({
            'token': token,
        }, status.HTTP_200_OK) 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from util.response import ErrorResponseTemplates
from wallet.serializers import RechargeSerializer
from wallet.views.decorators import recharge_exists, active_wallet_required
from account.auth import TokenAuthentication, SignedTokenAuthentication

class VerifyRecharge(APIView):
    authentication_classes = [TokenAuthentication, SignedTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @recharge_exists
    @active_wallet_required
    def post(self, request, recharge_id):
        
        try:
            payment_id = request.data['payment_id']
            signature = request.data['signature']

        except KeyError:
            return ErrorResponseTemplates.BAD_REQUEST()
        
        # verify and update
        if not request.recharge.verify_signature(payment_id, signature):
            return ErrorResponseTemplates.BAD_REQUEST('Invalid signature')

        recharge_serializer = RechargeSerializer(request.recharge)

        return Response({
            **recharge_serializer.data,
        }, status.HTTP_200_OK)
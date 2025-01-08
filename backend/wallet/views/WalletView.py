from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from wallet.serializers import WalletSerializer
from wallet.views.decorators import wallet_required

class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    @wallet_required
    def get(self, request):
        """Returns Wallet data
        """
        return Response(WalletSerializer(request.user.wallet).data)

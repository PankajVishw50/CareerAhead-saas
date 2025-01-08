from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from wallet.views.decorators import recharge_exists
from wallet.serializers import RechargeSerializer
from wallet.models import Recharge
from account.auth import TokenAuthentication, SignedTokenAuthentication

class RechargeView(APIView):
    authentication_classes = [TokenAuthentication, SignedTokenAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer] 
    template_name = 'wallet/recharge_template.html'

    # @recharge_exists
    def get(self, request, recharge_id):
        # serialized_data = RechargeSerializer(request.recharge)
        serialized_data = RechargeSerializer(Recharge.objects.get(id=recharge_id))
        return Response(serialized_data.data, 200)

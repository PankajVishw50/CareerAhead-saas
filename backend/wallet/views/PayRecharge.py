from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from util.response import ErrorResponseTemplates

class PayRecharge(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, order_id):
        pass 
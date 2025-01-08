from rest_framework.response import Response
from rest_framework.views import APIView

from wallet.razorpay import RazorPayWebhookHandler, RazorPayAuthentication
from util.response import ErrorResponseTemplates

class RazorpayWebhookView(APIView):
    authentication_classes = [RazorPayAuthentication]

    def post(self, request):

        print('Webhook Request came: ', request)

        handler = RazorPayWebhookHandler(request)
        response = handler.handle()

        if not isinstance(response, Response):
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()

        return response
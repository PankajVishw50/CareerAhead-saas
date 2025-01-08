from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 
from rest_framework.renderers import JSONRenderer, HTMLFormRenderer
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin


from util.response import ErrorResponseTemplates
from wallet.razorpay import razorpay
from wallet.models import Recharge
from wallet.serializers import RechargeSerializer
from wallet.views.decorators import active_wallet_required
from util.helpers import get_page_meta
from util.decorators import get_pagination_params
from account.auth import TokenAuthentication


class RechargesView(APIView):
    permission_classes = [IsAuthenticated]

    @active_wallet_required
    def post(self, request):
        try:
            amount = int(request.data['amount'])

            # Doesn't support other currencies at moment
            currency = razorpay.DEFAULT_CURRENCY
        except (KeyError, ValueError):
            return ErrorResponseTemplates.BAD_REQUEST('Invalid Payload')

        # Create order
        order, response = razorpay.create_order(amount, currency)

        if not order:
            return response
        
        # Create order object
        try:
            recharge = Recharge.objects.create_recharge(
                user=request.user,
                wallet=request.user.wallet,
                amount=response['amount'],
                currency=response['currency'],
                order_id=response['order_id'],
            )
        except:
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()
        
        recharge_serialized = RechargeSerializer(recharge)

        return Response({
            **recharge_serialized.data,
        }, status.HTTP_201_CREATED)

    @get_pagination_params
    def get(self, request):
        # import ipdb;ipdb.set_trace()

        paginator = Paginator(request.user.recharge_set.all(), request.pagination.size)
        try:
            page = paginator.page(request.pagination.page)
        except EmptyPage:
            return ErrorResponseTemplates.PAGINATION_NOT_FOUND(paginator.num_pages)
        
        serialized_data = RechargeSerializer(page.object_list, many=True)
        return Response({
            'meta': get_page_meta(paginator, page),
            'items': serialized_data.data,
        })
    
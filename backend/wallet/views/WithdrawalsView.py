from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from util.response import ErrorResponseTemplates
from wallet.razorpay import razorpay
from wallet.models import Withdrawal
from wallet.serializers import WithdrawalSerializer
from wallet.views.decorators import active_wallet_required
from util.decorators import get_pagination_params
from util.helpers import get_page_meta

class WithdrawalsView(APIView):
    permission_classes = [IsAuthenticated]

    @active_wallet_required
    def post(self, request): 
        try:
            amount = int(request.data['amount'])
            fund_account_id = request.data['fund_account_id']
        except (KeyError, ValueError):
            return ErrorResponseTemplates.BAD_REQUEST('Invalid Payload')

        # Validate amount
        if not Withdrawal.objects.validate_amount(amount): 
            return ErrorResponseTemplates.BAD_REQUEST(
                f'Value must be between the range of {settings.MINIMUM_WITHDRAWL} <= amount >= {settings.MAXIMUM_WITHDRAWL}.'
            )
        
        # validate if there is enough balance in wallet
        if not request.user.wallet.have_balance(amount):
            return ErrorResponseTemplates.BAD_REQUEST('Not enough balance in wallet')


        # Check if fund account is valid and
        success, response = razorpay.fetch_fund_account_by_id(fund_account_id)
        if not success:
            return response
        
        mode = None
        match response['account_type']:
            case 'vpa':
                mode = razorpay.FundTransferChoices.UPI
            case 'bank_account':
                mode = razorpay.FundTransferChoices.IMPS
            case 'card':
                mode = razorpay.FundTransferChoices.CARD
            case _:
                return ErrorResponseTemplates.BAD_REQUEST('Invalid fund account')
            
        
        
        # validate fund account is valid and belongs to current user
        if (
            response['id'] != fund_account_id 
            or response['contact_id'] != request.user.wallet.contact_id
            or response['active'] == False
        ):
            return ErrorResponseTemplates.BAD_REQUEST()        

        # Create Payout
        # Create withdrawl
        withdrawal = request.user.wallet.withdraw(amount)

        if not withdrawal:
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()

        payout, response = razorpay.create_payout(amount, fund_account_id, mode)

        if not payout:
            withdrawal.delete()
            return response 
        
        withdrawal.payout_id = response['id']
        withdrawal.save()

        if not withdrawal:
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()
        
        return Response(
            WithdrawalSerializer(withdrawal).data,
            status.HTTP_200_OK            
        )

    @get_pagination_params
    def get(self, request):

        paginator = Paginator(request.user.wallet.withdrawal_set.all(), request.pagination.size)

        try:
            page = paginator.page(request.pagination.page)
        except EmptyPage:
            return ErrorResponseTemplates.PAGINATION_NOT_FOUND(paginator.num_pages)
        
        serialized_data = WithdrawalSerializer(page.object_list, many=True)
        return Response({
            'meta': get_page_meta(paginator, page),
            'items': serialized_data.data,
        })
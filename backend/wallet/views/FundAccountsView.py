from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from rest_framework import status 
from rest_framework.response import Response
import requests 

from util.response import ErrorResponseTemplates
from wallet.razorpay import razorpay
from wallet.serializers import FundAccountSerializer
from wallet.views.decorators import active_wallet_required
from util.decorators import get_pagination_params

class FundAccountsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @get_pagination_params
    @active_wallet_required
    def get(self, request):

        # Convert page and size to count and skip
        count = request.pagination.size
        skip = (request.pagination.page-1) * request.pagination.size
        
        try:
            # Fetch funds detail from Razorpay
            response = requests.get(
                razorpay.API_GET_FUND_ACCOUNTS,
                headers={
                    'Authorization': razorpay.auth_digest_header
                },
                params={
                    'contact_id': request.user.wallet.contact_id,
                    'count': count,
                    'skip': skip,
                }
            )
            response.raise_for_status()
            json = response.json()
        except requests.HTTPError:
            return ErrorResponseTemplates.BAD_GATEWAY()
        except Exception as e:
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()

        serialized_data = FundAccountSerializer(json.get('items', []), many=True)
        
        return Response({
            'meta': {
                'currentItems': json.get('count'),
                'page': request.pagination.page,
                'size': request.pagination.size,
            },
            'items': serialized_data.data,
        }, status=status.HTTP_200_OK)

    @active_wallet_required
    def post(self, request):
        # import ipdb;ipdb.set_trace()
        account = FundAccountSerializer(data={**request.data, 'contact_id': request.user.wallet.contact_id})

        if not account.is_valid():
            return ErrorResponseTemplates.BAD_REQUEST(message='Invalid Payload', data={'errors': account.errors})

        created, response, *other = razorpay.create_fund_account(account.data)

        if not created:
            return response

        account = FundAccountSerializer(response)
        return Response(account.data, other[0].status_code)
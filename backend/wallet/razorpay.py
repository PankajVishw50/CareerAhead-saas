from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.apps import apps
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
import base64
import requests
import hmac
import hashlib

from util.helpers import generate_random_string
from util.response import ErrorResponseTemplates, response_error
from wallet.models import Withdrawal, Recharge

class RazorPay:
    USERNAME = settings.RAZORPAY_USERNAME
    SECRET = settings.RAZORPAY_SECRET
    BANKING_ACCOUNT_NUMBER = settings.RAZORPAY_BANKING_ACCOUNT_NUMBER

    class FundTransferChoices:
        UPI = 'UPI'
        IMPS = 'IMPS'
        NEFT = 'NEFT'
        RTGS = 'RTGS'
        CARD = 'CARD'

    DEFAULT_CURRENCY = 'INR'

    API_CREATE_ORDER = 'https://api.razorpay.com/v1/orders'
    API_CREATE_CONTACT = 'https://api.razorpay.com/v1/contacts'
    API_GET_FUND_ACCOUNTS = 'https://api.razorpay.com/v1/fund_accounts'
    API_GET_FUND_ACCOUNT = 'https://api.razorpay.com/v1/fund_accounts/:id'
    API_CREATE_FUND_ACCOUNT = 'https://api.razorpay.com/v1/fund_accounts'

    API_CREATE_PAYOUT = 'https://api.razorpay.com/v1/payouts'

    def __init__(self, username=None, secret=None):
        self.username = username or self.USERNAME
        self.secret = secret or self.SECRET

        self.digest = base64.b64encode(
            (f"{self.username}:{self.secret}").encode()
        ).decode()

        self.auth_digest_header = f"Basic {self.digest}"

    def create_order(self, amount, currency, **kwargs):
        data = {
            'amount': amount,
            'currency': currency,
            **kwargs,
        }

        try:
            response = (
                requests.post(
                    self.API_CREATE_ORDER,
                    headers={
                        'Authorization': self.auth_digest_header
                    },
                    json=data
                )
            )
            response.raise_for_status()
            data = response.json()
        except requests.HTTPError:
            return (False, ErrorResponseTemplates.BAD_REQUEST())
        except Exception as error:
            return (False, ErrorResponseTemplates.INTERNAL_SERVER_ERROR())

        response_data = {
            'order_id': data['id'],
            'currency': data['currency'],
            'amount': data['amount'],
            'status': data['status'], 
        } 

        return (True, response_data)

    def create_fund_account(self, data):
        try:
            response = requests.post(
                self.API_CREATE_FUND_ACCOUNT,
                headers={
                    'Authorization': self.auth_digest_header,
                },
                json=data,
            )
            response.raise_for_status()
            json = response.json()
        except requests.HTTPError:
            return (False, ErrorResponseTemplates.BAD_REQUEST())
        except:
            return (False, ErrorResponseTemplates.INTERNAL_SERVER_ERROR())
        
        return (True, json, response)
        

    def verify_signature(self, order_id, payment_id, signature):
        digest = hmac.new(
            self.SECRET.encode(),
            (f"{order_id}|{payment_id}").encode(),
            hashlib.sha256
        )
        
        if digest.hexdigest() != signature:
            return False 
        
        return True

    def create_contact(self, user):
        
        data = {
            'name': user.name or user.email.split('@')[0] + '_' + user.id.hex[:8],
            'email': user.email,
            'type': 'customer',
        }

        try:
            response = requests.post(
                self.API_CREATE_CONTACT,
                headers={
                    'Authorization': self.auth_digest_header,
                },
                json=data
            )
            response.raise_for_status()
            data = response.json()
            if not data or not data.get('id'):
                raise Exception('Failed to create customer')
        except Exception as e:
            return False

        return data['id']

    def fetch_fund_account_by_id(self, id):
        try:
            response = requests.get(
                self.API_GET_FUND_ACCOUNT.replace(':id', id),
                headers={
                    'Authorization': self.auth_digest_header,
                }
            )
            response.raise_for_status()
            json = response.json()
        except requests.exceptions.HTTPError:
            if response.status_code == 404:
                return (False, ErrorResponseTemplates.NOT_FOUND())

            return (False, ErrorResponseTemplates.BAD_REQUEST())
        except requests.exceptions.Timeout:
            return (False, response_error(status.HTTP_504_GATEWAY_TIMEOUT, 'Timeout'))
        except:
            return (False, ErrorResponseTemplates.INTERNAL_SERVER_ERROR())

        return (True, json)

    def create_payout(self, amount, fund_account_id, mode):
        data = {
            'account_number': self.BANKING_ACCOUNT_NUMBER,
            'fund_account_id': fund_account_id,
            'amount': amount,
            'currency': self.DEFAULT_CURRENCY,
            'mode': mode,
            'purpose': 'payout',
            'queue_if_low_balance': False
        }

        try:
            response = requests.post(
                self.API_CREATE_PAYOUT,
                headers={
                    'Authorization': self.auth_digest_header,
                },
                json=data
            )
            response.raise_for_status()
            json = response.json()

            if not json or not json.get('id'):
                raise requests.exceptions.HTTPError()

        except requests.exceptions.HTTPError:
            return (False, ErrorResponseTemplates.BAD_REQUEST())
        except:
            return (False, ErrorResponseTemplates.INTERNAL_SERVER_ERROR())

        return (True, json)


class RazorPayAuthentication(BaseAuthentication):
    RAZORPAY_WEBHOOK_SECRET = settings.RAZORPAY_WEBHOOK_SECRET
    def authenticate(self, request):
        try:
            # get header signature
            rz_signature = request.headers['X-Razorpay-Signature']

            # Generate signature
            signature = hmac.new(
                self.RAZORPAY_WEBHOOK_SECRET.encode(),
                request.body,
                hashlib.sha256,
            ).hexdigest()

            # Compare
            if not hmac.compare_digest(rz_signature, signature):
                raise AuthenticationFailed()
            
        except:
            raise AuthenticationFailed('Invalid signature')
    
        return (AnonymousUser(), signature)
    
class RazorPayWebhookHandler:

    def __init__(self, request):
        self.request = request

    def payout_processed(self):
        # get payload

        payout_data = self.request.data['payload']['payout']['entity']

        # Check is there is any withdrawal for this
        try:
            withdrawal = Withdrawal.objects.get(payout_id=payout_data['id'])
        except Withdrawal.DoesNotExist:
            return ErrorResponseTemplates.NOT_FOUND()
        
        # Update withdrawal state
        try:
            if not withdrawal.withdrawal_done():
                return ErrorResponseTemplates.BAD_REQUEST()
        except:
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()
        
        return Response(None, status.HTTP_200_OK)
    

    def payout_failed(self):

        # get payload
        payout_data = self.request.data['payload']['payout']['entity']

        # Check is there is any withdrawal for this
        try:
            withdrawal = Withdrawal.objects.get(payout_id=payout_data['id'])
        except Withdrawal.DoesNotExist:
            return ErrorResponseTemplates.NOT_FOUND()
        
        # Update withdrawal state
        try:
            if not withdrawal.withdrawal_failed():
                return ErrorResponseTemplates.BAD_REQUEST()
        except:
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()
        
        return Response(None, status.HTTP_200_OK)

    def order_paid(self):
        #get payload
        payment_payload = self.request.data['payload']['payment']['entity']

        # Check if provided order is valid 
        try:
            order = Recharge.objects.get(order_id=payment_payload['order_id'])
        except Recharge.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(None, status.HTTP_400_BAD_REQUEST)
        
        if order.amount != payment_payload['amount']:
            return Response(None, status.HTTP_400_BAD_REQUEST)
        
        if not order.complete_payment(payment_payload['id']):
            return Response(None, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(None, status.HTTP_200_OK)

        


                
    def handle(self):
        print('Webhook request Came: ', self.request.data['event'])

        if not self.request.data.get('event'):
            return ErrorResponseTemplates.BAD_REQUEST()

        match self.request.data['event']:
            case 'payout.processed': 
                return self.payout_processed()
            case event if event in ['payout.failed', 'payout.reversed', 'payout.rejected', 'payout.canceled']:
                return self.payout_failed()
            case 'order.paid':
                return self.order_paid()
            case _:
                return ErrorResponseTemplates.NOT_FOUND()


razorpay = RazorPay()


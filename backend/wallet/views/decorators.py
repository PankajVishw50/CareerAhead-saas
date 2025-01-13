from django.core.exceptions import ValidationError

from wallet.models import Recharge
from util.response import ErrorResponseTemplates

def recharge_exists(func):
    def wrapper(self, request, recharge_id, *args, **kwargs):
        try:
            # check if recharge_id is valid
            recharge = request.user.wallet.recharge_set.get(id=recharge_id)
        except Recharge.DoesNotExist:
            return ErrorResponseTemplates.NOT_FOUND('Recharge Not found')
        except ValidationError:
            return ErrorResponseTemplates.BAD_REQUEST()
        request.recharge = recharge

        return func(self, request, recharge_id, *args, **kwargs)
    return wrapper

def wallet_required(func):
    def wrapper(self, request, *args, **kwargs):
        if not (
            hasattr(self.request, 'user')
            and self.request.user.is_authenticated
            and hasattr(self.request.user, 'wallet')
        ):
            return ErrorResponseTemplates.NOT_FOUND('wallet not found')
        return func(self, request, *args, **kwargs)
    return wrapper

def active_wallet_required(func):
    def wrapper(self, request, *args, **kwargs):
        if not (
            hasattr(self.request, 'user')
            and self.request.user.is_authenticated
            and hasattr(self.request.user, 'wallet')
            and self.request.user.wallet.is_active
            and self.request.user.wallet.contact_id
        ):
            return ErrorResponseTemplates.FORBIDDEN('please activate your wallet first.')
        return func(self, request, *args, **kwargs)
    return wrapper


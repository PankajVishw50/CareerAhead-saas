from django.core.exceptions import ValidationError

from counselling.models import Counsellor, Slot
from util.response import ErrorResponseTemplates

def counsellor_exists(func):
    def wrapper(self, request, counsellor_id, *args, **kwargs):
        try:
            counsellor = Counsellor.objects.get(id=counsellor_id)
        except Counsellor.DoesNotExist:
            return ErrorResponseTemplates.NOT_FOUND("Counsellor Not found")
        except ValidationError:
            return ErrorResponseTemplates.BAD_REQUEST()
        
        request.counsellor = counsellor
        return func(self, request, counsellor_id, *args, **kwargs)
    return wrapper 


def is_user_counsellor(func):
    def wrapper(self, request, counsellor_id, *args, **kwargs):
        if request.user != request.counsellor.user:
            return ErrorResponseTemplates.FORBIDDEN('You are not allowed to access this resource')
        return func(self, request, counsellor_id, *args, **kwargs)
    return wrapper


def slot_exists(func):
    def wrapper(self, request, counsellor_id, slot_id, *args, **kwargs):
        try:
            slot = Slot.objects.get(id=slot_id)
        except Slot.DoesNotExist:
            return ErrorResponseTemplates.NOT_FOUND("Slot Not found")
        except ValidationError:
            return ErrorResponseTemplates.BAD_REQUEST()
        
        request.slot = slot
        return func(self, request, counsellor_id, slot_id, *args, **kwargs)
    return wrapper 


def slot_valid_exists(func):
    def wrapper(self, request, counsellor_id, slot_id, *args, **kwargs):
        try:
            slot = Slot.objects.get_valid(id=slot_id)
        except Slot.DoesNotExist:
            return ErrorResponseTemplates.NOT_FOUND("Slot Not found")
        except ValidationError:
            return ErrorResponseTemplates.BAD_REQUEST()
        
        request.slot = slot
        return func(self, request, counsellor_id, slot_id, *args, **kwargs)
    return wrapper 
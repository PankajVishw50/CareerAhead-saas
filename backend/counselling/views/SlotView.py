from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from util.response import ErrorResponseTemplates
from counselling.models import Slot
from counselling.views.decorators import (
    counsellor_exists,
    slot_valid_exists,
    is_user_counsellor,
)
from counselling.serializers import SlotSerializer


class SlotView(APIView):
    permission_classes = [IsAuthenticated]

    @counsellor_exists
    @is_user_counsellor
    @slot_valid_exists
    def delete(self, request, counsellor_id, slot_id):

        if not request.slot.delete():
            return ErrorResponseTemplates.INTERNAL_SERVER_ERROR()

        slot_s = SlotSerializer(request.slot)
        return Response(slot_s.data)

    @counsellor_exists
    @is_user_counsellor
    @slot_valid_exists
    def patch(self, request, counsellor_id, slot_id):

        try:
            operation = request.data["disable"]

            if not isinstance(operation, bool):
                return ErrorResponseTemplates.BAD_REQUEST(
                    "Invalid payload - `disable` should be an valid value"
                )
        except KeyError:
            return ErrorResponseTemplates.BAD_REQUEST(
                "Invalid payload - `disable` should be passed"
            )

        if operation is True:
            request.slot.deactivate()
        else:
            request.slot.activate()

        slot_s = SlotSerializer(request.slot)
        return Response(slot_s.data)

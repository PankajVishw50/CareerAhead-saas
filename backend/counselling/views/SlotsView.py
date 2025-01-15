from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db.models import Q
import datetime

from util.response import ErrorResponseTemplates
from counselling.models import Slot
from counselling.serializers import SlotSerializer
from counselling.views.decorators import counsellor_exists, is_user_counsellor

class SlotsView(APIView):
    permission_classes = [IsAuthenticated]

    @counsellor_exists
    @is_user_counsellor
    def post(self, request, counsellor_id):
        # import ipdb;ipdb.set_trace()

        try:
            slots = request.data

            if isinstance(slots, dict):
                slots = [slots]

            if not isinstance(slots, list):
                return ErrorResponseTemplates.BAD_REQUEST("Invalid Payload - slots")

            # Sort Slots by start_time
            slots.sort(key=lambda x: datetime.datetime.strptime(x['from_time'], settings.FORMAT_TIME))


        except KeyError:
            return ErrorResponseTemplates.BAD_REQUEST("Valid Slots required")
        except ValueError as e:
            return ErrorResponseTemplates.BAD_REQUEST("Invalid slot value: %s" % e)


        slots_s = SlotSerializer(data=slots, many=True)
        if not slots_s.is_valid():
            return ErrorResponseTemplates.BAD_REQUEST("Invalid payload", {"errors": slots_s.errors})            

        # Check if no slot conflict with each other
        for i, slot in enumerate(slots_s.validated_data[1:]):
            last_end_time = (datetime.datetime.combine(
                datetime.datetime.today().date(), slots_s.validated_data[i]['from_time']
            ) + slots_s.validated_data[i]['duration']).time()

            if last_end_time > slot['from_time']:
                return ErrorResponseTemplates.CONFLICT(
                    "Slots are Conflicting."
                    "Make sure no slots are overlapping"
                )

        # Check if slot count is not more than SLOT_MAX_COUNT
        if (total_slot_c := len(slots_s.validated_data) + request.counsellor.slots.count()) > settings.SLOT_MAX_COUNT:
            return ErrorResponseTemplates.BAD_REQUEST(
                f"Maximum {settings.SLOT_MAX_COUNT} slots are allowed. "
                f"Your slots count: {total_slot_c}. "
                f"Either flush unused slots or delete slots",
            )


        # Check database
        query = request.counsellor.slots.filter(is_active=True)
        filters = Q()

        for slot in slots_s.validated_data:
            end_time = (
                datetime.datetime.combine(
                    datetime.datetime.today().date(), slot['from_time']
                )
                + slot['duration']
            ).time()

            filters |= Q(from_time__range=(slot['from_time'], end_time))
                    
        if query.filter(filters).count() > 0:
            return ErrorResponseTemplates.CONFLICT(
                "Slots are Conflicting."
                "Make sure no slots are overlapping"
            )

        # Check if user is counsellor
        slots_s.save(counsellor=request.counsellor, is_active=True,  timezone=request.counsellor.timezone)
        return Response(slots_s.data)
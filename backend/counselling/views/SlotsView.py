from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from django.conf import settings
from django.db.models import Q, F
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
import datetime
from rest_framework import status

from util.response import ErrorResponseTemplates
from util.decorators import get_pagination_params
from counselling.models import Slot, Counsellor
from counselling.serializers import SlotSerializer
from counselling.views.decorators import counsellor_exists, is_user_counsellor, slot_valid_exists
from counselling.filters import SlotsModelFilterSet
from util.helpers import paginated_response
from util.mixins import OrderingMixin

class SlotsView(APIView, OrderingMixin):
    permission_classes = [IsAuthenticated]
    ordering_fields = ["created_at", "from_time", "duration", "fee"]
    ordering = ["from_time"]
    
    @get_pagination_params
    @counsellor_exists
    @is_user_counsellor
    def get(self, request, counsellor_id):
        slots = request.counsellor.slots.all_valids().filter(timezone=request.counsellor.timezone).order_by('from_time')
        slots_filtered = SlotsModelFilterSet(request.GET, queryset=slots)
        slots_filter = slots_filtered.qs
        slots_ordered = self.apply_ordering(request, slots_filter)
        paginator = Paginator(slots_ordered, request.pagination.size)
        try:
            page = paginator.page(request.pagination.page)
        except EmptyPage:
            return ErrorResponseTemplates.PAGINATION_NOT_FOUND(paginator.num_pages)
        
        slots_s = SlotSerializer(page, many=True)
        return Response(paginated_response(page, slots_s.data))
    

    @counsellor_exists
    @is_user_counsellor
    def post(self, request, counsellor_id):
        try:
            slots = request.data

            if not slots:
                return ErrorResponseTemplates.BAD_REQUEST("Atleast one slot is required")

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

        # import ipdb;ipdb.set_trace()
        # Check database
        query = request.counsellor.slots.filter(is_active=True)
        query = query.annotate(to_time=F("from_time") + F("duration"))
        filters = Q()


        # import ipdb;ipdb.set_trace()
        for slot in slots_s.validated_data:
            end_time = (
                datetime.datetime.combine(
                    datetime.datetime.today().date(), slot['from_time']
                )
                + slot['duration']
            ).time()

            filters |= Q(from_time__range=(slot['from_time'], end_time))
            filters |= Q(to_time__range=(slot["from_time"], end_time))
                    
        if query.filter(filters).count() > 0:
            return ErrorResponseTemplates.CONFLICT(
                "Slots are Conflicting."
                "Make sure no slots are overlapping"
            )

        # Check if user is counsellor
        slots_s.save(counsellor=request.counsellor, is_active=True,  timezone=request.counsellor.timezone)

        return Response(slots_s.data, status.HTTP_201_CREATED)
    
    @counsellor_exists
    @is_user_counsellor
    def delete(self, request, counsellor_id):
        # import ipdb;ipdb.set_trace()
        count = 0
        if request.data.get('disabled'):
            if request.data.get('disabled') is not True:
                return ErrorResponseTemplates.BAD_REQUEST('`disabled` can not be False')

            count, _ = request.counsellor.slots.all_valids().delete()
            
        elif request.data.get("slots"):
            req_slots = request.data.get("slots")
            
            if not isinstance(req_slots, list):
                return ErrorResponseTemplates.BAD_REQUEST("Invalid payload - `slots` must be array of slots id")

            filters = Q()
            for slot in req_slots:
                filters |= Q(id=slot)
        

            with transaction.atomic():
                query = request.counsellor.slots.all_valids().filter(filters)
                count, _ = query.delete()

                if count != len(req_slots):
                    transaction.set_rollback(True)
                    return ErrorResponseTemplates.BAD_REQUEST("All slots ids must be valid")

        return Response({
            "total": count,
        })


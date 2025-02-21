from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import pytz
import datetime
from django.test.utils import override_settings
from django.db.models import (
    Q, F, Case,
    When, ExpressionWrapper, Value,
    DateTimeField, TimeField, OuterRef,
    Exists, Subquery,  Func, IntegerField,
    SmallIntegerField, 
)
from django.db.models.functions import ExtractWeekDay, Cast
from rest_framework import status
from django.utils import timezone as django_timezone

from counselling.views.decorators import counsellor_exists
from util.response import ErrorResponseTemplates
from counselling.models import Slot
from counselling.serializers import AvailableSlotSerializer


class AvailableSlotsView(APIView):
    permission_classes = [IsAuthenticated]

    @counsellor_exists
    def get(self, request, counsellor_id):
        try:
            timezone = request.query_params.get("timezone", "UTC")
            tz = pytz.timezone(timezone)
            dates = request.query_params.getlist("dates") 

            if len(dates) == 0:
                return ErrorResponseTemplates.BAD_REQUEST(f"Dates can not be empty")
            elif len(dates) > settings.AVAILABLE_SLOT_MAX_FETCH:
                return ErrorResponseTemplates.BAD_REQUEST(f"Dates length can not be larger than {settings.AVAILABLE_SLOT_MAX_FETCH}")
            
        except pytz.exceptions.UnknownTimeZoneError:
            return ErrorResponseTemplates.BAD_REQUEST(f"Invalid timezone - {timezone}")

        output = dict()
        current_dt = datetime.datetime.now(pytz.utc)

        for date in dates:
            start_dt = None
            VALID_FORMATS = [settings.FORMAT_DATE, settings.FORMAT_DATETIME]
            for format in VALID_FORMATS:
                try:
                    start_dt = tz.localize(datetime.datetime.strptime(date, format))
                except ValueError:
                    pass
            
            if not start_dt:
                return ErrorResponseTemplates.BAD_REQUEST(
                    f"Invalid date format - `{date}` "  
                    f"Expected format: {VALID_FORMATS}"
                )

            end_dt = start_dt.replace(hour=23, minute=59, second=59)

            if end_dt < current_dt:
                return ErrorResponseTemplates.BAD_REQUEST(
                    f"Date must be in future"
                )

            # Convert it to counsellor's timezone
            start_dt = start_dt.astimezone(request.counsellor.tz)
            end_dt = end_dt.astimezone(request.counsellor.tz)  


            if start_dt.date() == end_dt.date():
                a_from_dt = start_dt
                a_to_dt = end_dt
                b_from_dt = b_to_dt = start_dt

            else:
                a_from_dt = start_dt
                a_to_dt = start_dt.replace(hour=23, minute=59, second=59)

                b_from_dt = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
                b_to_dt = end_dt


            a_from_t = a_from_dt.time()
            a_to_t = a_to_dt.time()

            b_from_t = b_from_dt.time()
            b_to_t = b_to_dt.time()

            a_day = a_from_dt.weekday()
            b_day = b_from_dt.weekday()

            with django_timezone.override(request.counsellor.tz):
                sub_query = request.counsellor.sessions.filter(
                    (
                        Q(from_datetime__gte=OuterRef("from_datetime"))
                        & Q(from_datetime__lt=OuterRef("to_datetime"))
                    )
                    | (
                        Q(to_datetime__gt=OuterRef("from_datetime"))
                        & Q(to_datetime__lt=OuterRef("to_datetime"))
                    )
                    | (
                        Q(from_datetime__lte=OuterRef("from_datetime"))
                        & Q(to_datetime__gt=OuterRef("from_datetime"))
                    )
                    | (
                        Q(from_datetime__lt=OuterRef("to_datetime"))
                        & Q(to_datetime__gte=OuterRef("to_datetime"))
                    )
                )

                # import ipdb;ipdb.set_trace()
                query = (
                    request.counsellor.slots.filter(
                        Q(is_deleted__isnull=True) | Q(is_deleted=False),
                        Q(from_time__range=(a_from_t, a_to_t))
                        | Q(from_time__range=(b_from_t, b_to_t)),
                        timezone=request.counsellor.timezone,
                        is_active=True
                    )
                    .annotate(
                        from_datetime=Case(
                            When(
                                Q(from_time__range=(a_from_t, a_to_t)),
                                then=ExpressionWrapper(
                                    F('from_time') 
                                    + request.counsellor.tz.localize(
                                        datetime.datetime.combine(a_from_dt.date(), datetime.datetime.min.time())
                                    ), 
                                    output_field=DateTimeField()
                                )
                            ),
                            When(
                                Q(from_time__range=(b_from_t, b_to_t)),
                                then=ExpressionWrapper(
                                    F('from_time') 
                                    + request.counsellor.tz.localize(
                                        datetime.datetime.combine(b_from_dt.date(), datetime.datetime.min.time()), 
                                    ),    
                                    output_field=DateTimeField())
                            ),
                        ),
                        to_datetime=F("from_datetime") + F("duration"),
                        from_datetime_day=Cast(ExpressionWrapper(
                            Func(
                                Value(2),
                                F("from_datetime__week_day") - Value(1),
                                function="POWER",
                                output_field=IntegerField(),
                            ),
                            output_field=IntegerField()
                        ), output_field=IntegerField())
                    )
                    .filter(
                        from_datetime_day=F("from_datetime_day").bitand(F("days"))
                    )
                    .exclude(
                        Q(Exists(sub_query))
                        | Q(from_datetime__lt=current_dt.astimezone(request.counsellor.tz))
                    )
                    .order_by("from_datetime")
                )
                # import ipdb;ipdb.set_trace() 
                output[date] = AvailableSlotSerializer(query, many=True).data

        return Response(output, status.HTTP_200_OK)
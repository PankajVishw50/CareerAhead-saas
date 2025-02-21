from django.conf import settings
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import datetime
import pytz 

from util.response import ErrorResponseTemplates
from counselling.views.decorators import counsellor_exists, slot_exists
from counselling.models import CounsellingSession
from wallet.views.decorators import active_wallet_required
from counselling.serializers import CounsellingSessionSerializer

class SessionsView(APIView):
    permission_classes = [IsAuthenticated]

    @active_wallet_required
    @counsellor_exists
    @slot_exists
    def post(self, request, counsellor_id, slot_id):
        # import ipdb;ipdb.set_trace()

        try:
            from_datetime = request.data['from_datetime']
            from_dt = datetime.datetime.strptime(from_datetime, settings.FORMAT_DATETIME_ZONE)
            
        except ValueError:
            return ErrorResponseTemplates.BAD_REQUEST(
                "Invalid Payload: valid `from_datetime` is required"
            )
        
        # Check balance
        if request.user.wallet.balance < request.slot.fee:
            return ErrorResponseTemplates.BAD_GATEWAY(
                "Insufficient balance"
            )

        # Check if this slot is valid
        c_from_dt = from_dt.astimezone(request.counsellor.tz) 

        if c_from_dt.time() != request.slot.from_time:
            return ErrorResponseTemplates.BAD_REQUEST("Invalid payload")
        
        if not request.slot.work_day(c_from_dt.weekday()):
            return ErrorResponseTemplates.BAD_REQUEST("Slot not valid for specified day")

        # Check if any slot with conflicted time exists
        u_from_dt = from_dt.astimezone(pytz.utc)
        u_to_dt = u_from_dt + request.slot.duration

        u_from_t = u_from_dt.time()
        u_to_t = u_to_dt.time()

        conflicted_slots = request.counsellor.sessions.filter(
            Q(from_datetime__range=(u_from_dt, u_to_dt)) 
            | Q(to_datetime__range=(u_from_dt, u_to_dt))
        ).count()

        if conflicted_slots > 0:
            return ErrorResponseTemplates.BAD_GATEWAY(
                "Slot is not available for specified date"
            )
        
        # Create a new session
        session = CounsellingSession.objects.create_session(
            request.user,
            request.counsellor,
            request.slot,
            from_dt,
        )

        return Response(CounsellingSessionSerializer(session).data)
 
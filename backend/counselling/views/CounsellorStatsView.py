from django.db.models import Sum
from django.forms import ValidationError
from rest_framework.views import APIView, Response

from account.models import User
from counselling.views.decorators import counsellor_exists
from util.response import ErrorResponseTemplates


class CounsellorStatsView(APIView):

    @counsellor_exists
    def get(self, request, _):
        data = {
            "total_sessions": request.counsellor.sessions.count(),
        }

        # Data exclusive to only authenticated counsellor
        if request.user == request.counsellor.user:
            data["total_earnings"] = request.counsellor.sessions.aggregate(
                total=Sum("slot__fee"),
            )["total"]
            data["upcoming_sessions"] = request.counsellor.upcoming_sessions.count()
            data["active_sessions"] = request.counsellor.active_sessions.count()
            data["old_sessions"] = request.counsellor.old_sessions.count()

        # Interaction between
        # counsellor and
        # current user (if counsellor != user)
        # or if user_id provided in query param (only if current user is counsellor)
        user = None
        if request.user != request.counsellor.user:
            user = request.user
        elif request.GET.get("user_id") and request.user == request.counsellor.user:
            try:
                user = User.objects.get(id=request.GET.get("user_id"))
            except (User.DoesNotExist, ValidationError):
                return ErrorResponseTemplates.NOT_FOUND(
                    f"Specified user_id:{request.GET.get("user_id")} is not valid"
                )

        if user:
            user_sessions = user.sessions.filter(counsellor=request.counsellor)
            data["user_interaction"] = {
                "total_sessions": user_sessions.count(),
                "total_earnings": user_sessions.aggregate(
                    total=Sum("slot__fee"),
                )["total"],
                "upcoming_sessions": request.counsellor.upcoming_sessions.filter(
                    user=user
                ).count(),
                "active_sessions": request.counsellor.active_sessions.filter(
                    user=user
                ).count(),
                "old_sessions": request.counsellor.old_sessions.filter(
                    user=user
                ).count(),
            }

        return Response(data)

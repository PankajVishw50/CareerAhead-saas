from django.urls import path, include
from counselling.views import (
    CounsellorStatsView,
    CounsellorView,
    AvailableSlotsView,
    SessionView,
    SessionsView,
    SlotsView,
    CounsellorSessionsView,
    CounsellorsListView,
    SlotView,
)

urlpatterns = [
    path("", CounsellorsListView.as_view(), name="counsellors"),
    path(
        "<uuid:counsellor_id>/",
        include(
            [
                path("", CounsellorView.as_view(), name="counsellor"),
                path("slots", SlotsView.as_view(), name="slots"),
                path("slot/<uuid:slot_id>", SlotView.as_view(), name="slot"),
                path(
                    "slots/available",
                    AvailableSlotsView.as_view(),
                    name="available-slots",
                ),
                path(
                    "slots/<uuid:slot_id>/sessions",
                    CounsellorSessionsView.as_view(),
                    name="schedule-session",
                ),
                path("stats", CounsellorStatsView.as_view(), name="counsellor-stats"),
            ]
        ),
    ),
    path("sessions/", SessionsView.as_view(), name="scheduled-sessions"),
    path("sessions/<uuid:pk>", SessionView.as_view(), name="scheduled-session"),
]

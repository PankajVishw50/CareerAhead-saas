from django.urls import path, include
from counselling.views import (
    CounsellorView,
    AvailableSlotsView, SlotsView,
    SessionsView, CounsellorsListView,
    SlotView,
)

urlpatterns = [
    path('', CounsellorsListView.as_view(), name='counsellors'),
    path("<uuid:counsellor_id>/", include([
        path('', CounsellorView.as_view(), name='counsellor'),
        path('slots', SlotsView.as_view(), name='slots'),
        path("slot/<uuid:slot_id>", SlotView.as_view(), name="slot"),
        path('slots/available', AvailableSlotsView.as_view(), name='available-slots'),
        path("slots/<uuid:slot_id>/sessions", SessionsView.as_view(), name='schedule-session')
    ]))
]
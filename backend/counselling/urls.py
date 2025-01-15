from django.urls import path, include
from counselling.views import (
    CounsellorsView, CounsellorView,
    AvailableSlotsView, SlotsView
)

urlpatterns = [
    path('', CounsellorsView.as_view(), name='counsellors'),

    path("<uuid:counsellor_id>/", include([
        path('', CounsellorView.as_view(), name='counsellor'),
        path('slots', SlotsView.as_view(), name='slots'),
        path('slots/available', AvailableSlotsView.as_view(), name='available-slots'),
    ]))
    
]
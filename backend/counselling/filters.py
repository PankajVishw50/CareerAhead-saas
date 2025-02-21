import django_filters
from django.db.models import F, Q, Value
from django.db.models.expressions import RawSQL

from counselling.models import Counsellor
from account.models import User
from counselling.models import Slot



class CounsellorModelFilterSet(django_filters.FilterSet):
    # age = django_filters.NumberFilter(field_name="user__age", lookup_expr="exact")
    # age_range = django_filters.RangeFilter(field_name="user__age")

    name = django_filters.CharFilter(field_name="user__name", lookup_expr="icontains")
    gender = django_filters.MultipleChoiceFilter(field_name="user__gender", choices=[(gender.name, gender.value) for gender in User.Genders])

    class Meta:
        model = Counsellor
        fields = {
            "timezone": ["iexact"],
        }

class SlotsModelFilterSet(django_filters.FilterSet):
    active = django_filters.BooleanFilter(field_name="is_active", lookup_expr="exact")
    day = django_filters.MultipleChoiceFilter(
        choices=[
            ("SU", "Sunday"), ("M", "Monday"),
            ("TU", "Tuesday"), ("W", "Wednesday"),
            ("TH", "Thursday"), ("F", "Friday"),
            ("SA", "Saturday")
        ],
        method="filter_by_day"
    )
    fee = django_filters.RangeFilter(field_name="fee")

    class Meta:
        model = Slot
        fields = {
        }

    DAYS_MAPPING = {
        "SU": 0b1, "M": 0b10, "TU": 0b100, "W": 0b1000, "TH": 0b10000, "F": 0b100000, "SA": 1000000
    }


    def filter_by_day(self, queryset, name, values):
        day_bits = [self.DAYS_MAPPING.get(day.strip()) for day in values if self.DAYS_MAPPING.get(day.strip()) is not None]

        return queryset.annotate(working_days=F("days").bitand(sum(day_bits))).filter(working_days__gt=0)
from rest_framework.filters import OrderingFilter


class OrderingMixin:
    ordering_filter = OrderingFilter()
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def apply_ordering(self, request, queryset):
        return self.ordering_filter.filter_queryset(request, queryset, self)

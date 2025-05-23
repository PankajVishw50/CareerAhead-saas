from rest_framework.pagination import CursorPagination

class GeneralCursorPagination(CursorPagination):
    ordering = ["-created_at"]
    page_size = 20
    page_size_query_param = "size" 
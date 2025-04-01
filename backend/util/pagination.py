from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from util.helpers import paginated_response

class BasePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"
    max_page_size = 40

    def get_paginated_response(self, data):
        from util.helpers import get_page_meta
        
        return Response(paginated_response(self.page, data))
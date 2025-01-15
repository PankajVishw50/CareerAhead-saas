from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response

from util.decorators import get_pagination_params
from util.helpers import get_page_meta
from counselling.models import Counsellor
from counselling.serializers import CounsellorSerializer
from util.response import ErrorResponseTemplates

class CounsellorsView(APIView):
    permission_classes = [IsAuthenticated]

    @get_pagination_params
    def get(self, request):
        paginator = Paginator(Counsellor.objects.all_valid(), request.pagination.size)

        try:
            page = paginator.page(request.pagination.page)
        except EmptyPage:
            return ErrorResponseTemplates.PAGINATION_NOT_FOUND(paginator.num_pages)
        
        serialized_data = CounsellorSerializer(page.object_list, many=True)
        return Response({
            "meta": get_page_meta(paginator, page),
            "items": serialized_data.data,
        })
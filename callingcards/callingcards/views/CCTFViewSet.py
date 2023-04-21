from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import CCTF
from ..serializers import CCTFSerializer, CCTFListSerializer


class CCTFViewSet(ListModelFieldsMixin,
                  CustomCreateMixin,
                  CustomValidateMixin,
                  UpdateModifiedMixin,
                  PageSizeModelMixin,
                  viewsets.ModelViewSet,
                  CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CCTF.objects.all().order_by('id')  # noqa
    serializer_class = CCTFSerializer  # noqa
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['get'], url_path='tf_list',
            url_name='tf-list')
    def tf_list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='tf_list/count',
            url_name='tf-list-count')
    def effects_count(self, request, *args, **kwargs) -> Response:
        return self.count(request, *args, **kwargs)

    @action(detail=False, url_path='tf_list/pagination_info',
            url_name='tf-list-pagination-info')
    def effects_pagination_info(self, request,
                                *args, **kwargs) -> Response:
        return self.pagination_info(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='tf_list/fields',
            url_name='tf-list-fields')
    def effects_fields(self, request, *args, **kwargs):
        filter_fields = None
        return self.fields(request, *args, filter_fields=filter_fields)

    def get_queryset(self):
        if 'tf_list' in self.request.path_info:
            return CCTF.objects.tf_list()
        else:
            return CCTF.objects.all().order_by('id')

    def get_serializer_class(self):
        if 'tf_list' in self.request.path_info:
            return CCTFListSerializer
        else:
            return CCTFSerializer
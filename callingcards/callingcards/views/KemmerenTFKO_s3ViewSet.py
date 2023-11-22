# pylint: disable=W1203
import logging
import gzip
from rest_framework import viewsets, status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import KemmerenTFKO_s3
from ..serializers import (KemmerenTFKO_s3Serializer,)
from ..filters import KemmerenTfko_s3Filter


logger = logging.getLogger(__name__)


class KemmerenTFKO_s3ViewSet(ListModelFieldsMixin,
                             CustomCreateMixin,
                             PageSizeModelMixin,
                             CountModelMixin,
                             UpdateModifiedMixin,
                             CustomValidateMixin,
                             viewsets.ModelViewSet):
    """
    API endpoint that allows KemmerenTFKO_s3 to be viewed or edited.
    """
    queryset = KemmerenTFKO_s3.objects.all().order_by('id')
    serializer_class = KemmerenTFKO_s3Serializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = KemmerenTfko_s3Filter
    search_fields = ('regulator__locus_tag', 'regulator__gene')

    def create(self, request, *args, **kwargs):

        logger.debug('USER: %s', request.user)
        logger.debug('TOKEN: %s', request.auth)
        logger.debug('HTTP_AUTH: %s', request.META.get('HTTP_AUTHORIZATION'))

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED)

        # Check that required fields for all upload methods are present
        required_fields = set(field.name for field in
                              KemmerenTFKO_s3._meta.get_fields()
                              if field.concrete and field.name not in
                              ['id', 'uploader', 'uploadDate',
                               'modified', 'modifiedBy'])

        if not set(request.data.keys()).issubset(required_fields):
            return Response({'error': 'Missing required field(s): {}'
                             .format(', '.join(required_fields -
                                               set(required_fields)))},
                            status=status.HTTP_400_BAD_REQUEST)
        
        token = str(request.auth)

        if not token:
            return Response(
                {'error': 'Auth Token not found -- contact admin.'},
                status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES.get('file')
        if uploaded_file is None:
            return Response({'error': 'file file not provided.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not uploaded_file.name.endswith('.csv.gz'):
            return Response({'error': 'file must be a .csv.gz file.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     with gzip.open(uploaded_file, 'rt') as f:
        #         df = pd.read_csv(f, sep="\t", index_col=False)
        # except UnicodeDecodeError as exc:
        #     return Response({'error': f'Error decoding file: {exc}'},
        #                     status=status.HTTP_400_BAD_REQUEST)

        # required_columns = {'chr', 'coord', 'YPD_Sig', 'YPD_Ctrl',
        #                     'YPD_log2Fold', 'YPD_log2P', 'ActiveConds'}
        # if not all(column in df.columns for column in required_columns):
        #     missing = required_columns - set(df.columns)
        #     return Response({'error': f'Missing required '
        #                      f'column(s): {", ".join(missing)}'},
        #                     status=status.HTTP_400_BAD_REQUEST)

        # Call the parent create() method with the modified request
        return super().create(request, *args, **kwargs)

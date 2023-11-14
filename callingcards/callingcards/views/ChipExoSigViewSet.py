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
from ..models import ChipExoSig
from ..serializers import (ChipExoSigSerializer,)
from ..filters import ChipExoSigregionsFilter
from ..utils import validate_bed6_df


logger = logging.getLogger(__name__)


class ChipExoSigViewSet(ListModelFieldsMixin,
                               CustomCreateMixin,
                               PageSizeModelMixin,
                               CountModelMixin,
                               UpdateModifiedMixin,
                               CustomValidateMixin,
                               viewsets.ModelViewSet):
    """
    API endpoint that allows ChipExoSig to be viewed or edited.
    """
    queryset = ChipExoSig.objects.all().order_by('id')
    serializer_class = ChipExoSigSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = ChipExoSigFilter
    search_fields = ('tf__locus_tag', 'tf__gene', 'time')

    def create(self, request, *args, **kwargs):

        logger.debug('USER: %s', request.user)
        logger.debug('TOKEN: %s', request.auth)
        logger.debug('HTTP_AUTH: %s', request.META.get('HTTP_AUTHORIZATION'))

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED)

        # Check that required fields for all upload methods are present
        key_check_diff = {'tf', 'chipexo_id',
                          'condition', 'parent_condition',
                          'file'} - set(request.data.keys())

        if key_check_diff:
            return Response({'error': 'Missing required field(s): {}'
                             .format(', '.join(key_check_diff))},
                            status=status.HTTP_400_BAD_REQUEST)

        token = str(request.auth)

        if not token:
            return Response({'error': 'Auth Token not found -- contact admin.'},  # noqa
                            status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES.get('file')
        if uploaded_file is None:
            return Response({'error': 'file file not provided.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not uploaded_file.name.endswith('.tsv.gz'):
            return Response({'error': 'file must be a .tsv.gz file.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            with gzip.open(uploaded_file, 'rt') as f:
                df = pd.read_csv(f, sep="\t", index_col=False)
        except UnicodeDecodeError as exc:
            return Response({'error': f'Error decoding file: {exc}'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            chr_format = validate_bed6_df(df)
        except ValueError as exc:
            return Response({'error': f'The file does not conform to bed6 '
                             f'format expectations. However, note that column '
                             f'headers must be provided (not typical for a '
                             f'bed file). Validation error: {exc}'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Call the parent create() method with the modified request
        return super().create(request, *args, **kwargs)

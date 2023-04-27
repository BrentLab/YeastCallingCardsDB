from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
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
from ..models import Hops_s3
from ..serializers import (Hops_s3Serializer,)
from ..filters import Hops_s3Filter
from ..utils.validate_qbed_upload import (validate_chromosomes,
                                          validate_coordinates,
                                          validate_strand)

class Hops_s3ViewSet(ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin,
                     viewsets.ModelViewSet):
    """
    API endpoint that allows Hops_s3 to be viewed or edited.
    """
    queryset = Hops_s3.objects.all()
    serializer_class = Hops_s3Serializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = Hops_s3Filter
    search_fields = ('experiment__tf__tf__id',
                     'experiment__tf__tf__locus_tag',
                     'experiment__tf__tf__gene',
                     'experiment_id',
                     'batch',
                     'batch_replicate',
                     'modifiedBy', 'createdBy', 'created', 'modified')

    def create(self, request, *args, **kwargs):
        # Check that the uploaded file has the correct format
        try:
            uploaded_file = request.FILES.get('qbed')
        except KeyError:
            return Response({'error': 'Qbed file not provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if uploaded_file.name.endswith('.gz') \
            | uploaded_file.name.endswith('.gzip') \
                | uploaded_file.name.endswith('.zip'):
            df = pd.read_csv(uploaded_file,
                             sep='\t',
                             compression='gzip',
                             header=None,
                             index_col=False)
        else:
            df = pd.read_csv(uploaded_file,
                             sep='\t',
                             header=None,
                             index_col=False)
        if df.shape[1] < 5:
            return Response({'error': ('File must have at least 5 columns, '
                                       'which should be "chr", "start", '
                                       '"end", "depth", "strand"')},
                            status=status.HTTP_400_BAD_REQUEST)
        validate_chr_tuple = validate_chromosomes(df)
        if validate_chr_tuple[0] is not None:
            return Response({'error': ('The following chromosomes in the '
                                       'uploaded file do not match any '
                                       'chromosomes in the database: '
                                       f'{validate_chr_tuple[1]}')},
                            status=status.HTTP_400_BAD_REQUEST)

        validate_coordinates_tuple = \
            validate_coordinates(df, validate_chr_tuple[0])
        
        if validate_coordinates_tuple[0] is not None:
            return Response({'error': ('The following coordinates in the '
                                       'uploaded file do not match any '
                                       'coordinates in the database: '
                                       f'{validate_coordinates_tuple[1]}')},
                            status=status.HTTP_400_BAD_REQUEST)

        validate_strand_list = validate_strand(df)
        if len(validate_strand_list) > 0:
            return Response({'error': ('The following strands in the '
                                       'uploaded file do not match any '
                                       'strands in the database: '
                                       f'{validate_strand_list}')},
                            status=status.HTTP_400_BAD_REQUEST)

        # Call the parent create() method to save the instance
        return super().create(request, *args, **kwargs)

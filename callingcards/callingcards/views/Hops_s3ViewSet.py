# pylint: disable=W1203
import logging
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.test import APIClient
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse
import pandas as pd
from .mixins import (ListModelFieldsMixin,
                     CustomCreateMixin,
                     PageSizeModelMixin,
                     CountModelMixin,
                     UpdateModifiedMixin,
                     CustomValidateMixin)
from ..models import Hops_s3, CCTF, CCExperiment, Gene, QcManualReview
from ..serializers import (Hops_s3Serializer,)
from ..filters import Hops_s3Filter
from ..utils.validate_qbed_upload import (validate_chromosomes,
                                          validate_coordinates,
                                          validate_strand)


logger = logging.getLogger(__name__)


def get_cctf_id(query_params_dict: dict, user_auth_token: str) -> int:
    """
    check if tf_gene or tf_locus_tag exists in query_params_dict. if so, 
    check to see if tf_strain exists. If either tf_gene or tf_locus_tag exists, 
    then try to get a CCTF object associated with that gene or locus_tag. If 
    tf_strain exists, use that info also. If a CCTF record does not exist, 
    create one, again using the strain info if it exists. Finally, return the
    CCTF id.

    :param query_params_dict: dictionary of query parameters
    :type query_params_dict: dict
    :param user_auth_token: user authentication token
    :type user_auth_token: str
    :return: id of CCTF object
    :rtype: int

    :raises RuntimeError: if the POST request fails to create a record
    """
    # extract relevant data from query_params_dict
    tf_gene = query_params_dict.get('tf_gene', None)
    tf_locus_tag = query_params_dict.get('tf_locus_tag', None)
    tf_strain = query_params_dict.get('tf_strain', None)

    # check if tf_gene or tf_locus_tag exists. If so, get CCTF object
    # if the CCTF object does not exist, set the gene_id variable
    if tf_gene:
        try:
            return CCTF.objects.get(tf__gene=tf_gene).id
        except CCTF.DoesNotExist:
            logger.info(f"No CCTF record exists for gene {tf_gene}")
            try:
                gene_id = Gene.objects.get(gene=tf_gene).id
            except Gene.DoesNotExist as exc:
                raise RuntimeError(f"Gene {tf_gene} does not exist "
                                   f"in database") from exc
    elif tf_locus_tag:
        try:
            return CCTF.objects.get(tf__locus_tag=tf_locus_tag).id
        except CCTF.DoesNotExist:
            logger.info(f"No CCTF record exists for locus_tag {tf_locus_tag}")
            try:
                gene_id = Gene.objects.get(locus_tag=tf_locus_tag).id
            except Gene.DoesNotExist as exc:
                raise RuntimeError(f"Gene {tf_locus_tag} does not exist "
                                   f"in database") from exc

    # if neither tf_gene or tf_locus_tag exists/is a valid gene, raise error
    else:
        raise ValueError('A valid tf_gene or tf_locus_tag must be provided')

    # if we have reached this point without returning, it means that there
    # is not a CCTF record for the gene, so we need to create one
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_auth_token}')

    # if the tf strain is passed, then use it
    if tf_strain:
        data = {'tf': gene_id,
                'strain': tf_strain}
        api_url = reverse('cctf-list')
        response = client.post(api_url, data)

        if response.status_code == status.HTTP_201_CREATED:
            # Return the id of the newly created CCExperiment object
            return response.data['id']
        else:
            raise RuntimeError(f"Failed to create CCTF instance "
                               f"through API endpoint {api_url}: "
                               f"{response.data}")

    # if the tf strain is not passed, then set to default value
    else:
        data = {'tf': gene_id}
        api_url = reverse('cctf-list')
        response = client.post(api_url, data)

        if response.status_code == status.HTTP_201_CREATED:
            # Return the id of the newly created CCExperiment object
            return response.data['id']
        else:
            raise RuntimeError(f"Failed to create CCTF instance "
                               f"through API endpoint {api_url}: "
                               f"{response.data}")


def get_ccexperiment_id(cctf_id: int,
                        batch: str,
                        batch_replicate: int,
                        lab: str,
                        user_auth_token: str) -> int:
    """
    Check to see if a CCExperiment object for a given cctf_id, batch and 
    batch_replicate exists. If it does, return the id of that object. If it 
    does not, create a new CCExperiment object and return the id of that 
    object.

    :param cctf_id: id of CCTF object
    :type cctf_id: int
    :param batch: batch name
    :type batch: str
    :param batch_replicate: batch replicate number
    :type batch_replicate: int
    :param user_auth_token: user authentication token   
    :type user_auth_token: str
    :return: id of CCExperiment object
    :rtype: int

    :raises RuntimeError: if the POST request fails to create a record
    """
    # check if CCExperiment object exists
    try:
        return CCExperiment.objects.get(tf=cctf_id,
                                        batch=batch,
                                        lab=lab,
                                        batch_replicate=batch_replicate).id
    except CCExperiment.DoesNotExist:
        logger.info(f"No CCExperiment record exists for tf {cctf_id}, "
                    f"batch {batch}, and batch_replicate {batch_replicate}. "
                    "Creating new CCExperiment record.")

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_auth_token}')

    # Prepare the request data
    data = {
        'tf': cctf_id,
        'batch': batch,
        'lab': lab,
        'batch_replicate': batch_replicate,
    }

    # Send the POST request
    api_url = reverse('ccexperiment-list')
    response = client.post(api_url, data)

    if response.status_code == status.HTTP_201_CREATED:
        # Return the id of the newly created CCExperiment object
        return response.data['id']
    else:
        raise RuntimeError(f"Failed to create CCExperiment "
                           f"through API endpoint {api_url}: {response.data}")


def create_manual_review(experiment_id: int, user_auth_token: str) -> int:
    """
    Given the experiment_id, create a QcManualReview record through the 
      DRF API

    :param experiment_id: id of CCExperiment object
    :type experiment_id: int
    :param user_auth_token: user authentication token
    :type user_auth_token: str
    :return: id of QcManualReview object
    :rtype: int

    :raises RuntimeError: if the POST request fails to create a record
    """
    try:
        return QcManualReview.objects.get(experiment=experiment_id).id
    except QcManualReview.DoesNotExist as exc:
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {user_auth_token}')

        # Prepare the request data
        data = {
            'experiment': experiment_id,
        }

        # Send the POST request
        api_url = reverse('qcmanualreview-list')
        response = client.post(api_url, data)

        if response.status_code == status.HTTP_201_CREATED:
            # Return the id of the newly created CCExperiment object
            return response.data['id']
        else:
            raise RuntimeError(f"Failed to create QcManualReview "
                               f"through API endpoint "
                               f"{api_url}: {response.data}") from exc


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
    permission_classes = [IsAuthenticated]
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

        logger.debug('USER: %s', request.user)
        logger.debug('TOKEN: %s', request.auth)
        logger.debug('HTTP_AUTH: %s', request.META.get('HTTP_AUTHORIZATION'))

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED)

        # Check that required fields for all upload methods are presen
        key_check_diff = {'chr_format', 'source'} - set(request.data.keys())

        if key_check_diff:
            return Response({'error': 'Missing required field(s): {}'
                             .format(', '.join(key_check_diff))},
                            status=status.HTTP_400_BAD_REQUEST)

        token = str(request.auth)

        if not token:
            return Response({'error': 'Auth Token not found -- contact admin.'},
                            status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES.get('qbed')
        if uploaded_file is None:
            return Response({'error': 'Qbed file not provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if uploaded_file.name.endswith('.gz') \
            | uploaded_file.name.endswith('.gzip') \
                | uploaded_file.name.endswith('.zip'):
            df = pd.read_csv(uploaded_file,
                             sep='\t',
                             compression='gzip',
                             index_col=False)
        else:
            df = pd.read_csv(uploaded_file,
                             sep='\t',
                             index_col=False)
        if list(df.columns) != ['chr', 'start', 'end', 'depth', 'strand']:
            return Response({'error': ('Qbed must have the following columns, '
                                       'in order:'
                                       ' ["chr", "start", '
                                       '"end", "depth", "strand"]')},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_chromosomes(df, request.data.get('chr_format'))
        except ValueError as exc:
            return Response({'error': str(exc)},
                            status=status.HTTP_400_BAD_REQUEST)

        validate_coordinates_list = \
            validate_coordinates(df, request.data.get('chr_format'))

        if validate_coordinates_list:
            return Response({'error': ('The following coordinates in the '
                                       'uploaded file do not match any '
                                       'coordinates in the database: '
                                       f'{validate_coordinates_list}')},
                            status=status.HTTP_400_BAD_REQUEST)

        validate_strand_list = validate_strand(df)
        if validate_strand_list:
            return Response({'error': ('The following strands in the '
                                       'uploaded file do not match any '
                                       'strands in the database: '
                                       f'{validate_strand_list}')},
                            status=status.HTTP_400_BAD_REQUEST)

        # Next, try to get the experiment_id from the query_params. If the
        # experiment ID is not passed, then create a new CCExperiment object
        # note that this may require the creation of a new CCTF object, also
        experiment_id = request.data.get('experiment')
        if not experiment_id:
            try:
                batch = request.data.get('batch')
            except KeyError:
                return Response({'error': 'Batch name not provided.'},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                batch_replicate = request.data.get('batch_replicate')
            except KeyError:
                return Response({'error':
                                 'Batch replicate number not provided.'},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                lab = request.data.get('lab')
            except KeyError:
                return Response({'error': 'Lab name not provided. The lab '
                                 'must already exist in the DB. If it '
                                 'does not, talk to the admin.'},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                cctf_id = get_cctf_id(request.data, token)
            except ValueError as exc:
                return Response({'error': str(exc)},
                                status=status.HTTP_400_BAD_REQUEST)

            experiment_id = get_ccexperiment_id(cctf_id,
                                                batch,
                                                batch_replicate,
                                                lab,
                                                token)

            request.data['experiment'] = experiment_id

        # check to see if a manaul review exists for this experiment. If it
        # does not, create one
        try:
            manual_review_id = create_manual_review(experiment_id,
                                                    token)
            logger.info(f"Qc manual review ID: {manual_review_id} "
                        f"for experiment: {experiment_id}")
        except RuntimeError as exc:
            return Response({'error': str(exc)},
                            status=status.HTTP_400_BAD_REQUEST)

        # drop unnecessary data from the request
        drop_keys = set(request.data.keys()) - {'chr_format',
                                                'source',
                                                'experiment',
                                                'qbed',
                                                'notes'}
        for key in drop_keys:
            del request.data[key]

        # Call the parent create() method with the modified request
        return super().create(request, *args, **kwargs)

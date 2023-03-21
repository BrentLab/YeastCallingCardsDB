from rest_framework.settings import api_settings
from django.conf import settings
import logging

from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ['ChrMapViewSet', 'GeneViewSet', 'PromoterRegionsViewSet',
           'HarbisonChIPViewSet', 'KemmerenTFKOViewSet', 'McIsaacZEVViewSet',
           'BackgroundViewSet', 'CCTFViewSet', 'CCExperimentViewSet',
           'HopsViewSet', 'HopsReplicacteSigViewSet', 'QcMetricsViewSet',
           'QcManualReviewViewSet', 'QcR1ToR2ViewSet',
           'QcR2ToR1ViewSet', 'QcTfToTransposonViewSet']


class CustomCreateMixin:
    """
    By default the user field is "user" you can change it
    to your model "user" field.
    cite: https://xploit29.com/2016/09/15/django-rest-framework-auto-assign-current-user-on-creation/

    Usage:
    class PostViewSet(CustomCreateMixin, PageSizeModelMixin, 
                      viewsets.ModelViewSet, CountModelMixin):
        # ViewsSet required info...
        user_field = 'creator'
    """

    _user_field = None

    @property
    def user_field(self):
        """user field is the field from the model that will be
          set to the current user. defaults to "uploder" """
        return self._user_field or 'uploader'

    @user_field.setter
    def user_field(self, value):
        self._user_field = value

    def create(self, request, *args, **kwargs):
        """ overwrite default create to accept either single or mulitple 
        records on create/update
            cite: https://stackoverflow.com/a/65078963/9708266
            accept either an array or a single object, 
            eg {"field1": "", "field2": "", ...} or 
            [{"field1": "", "field2": "", ...}, 
            {"field1": "", "field2": "", ...}, ...]
        """
        many_flag = True if isinstance(request.data, list) else False

        kwargs = {
            self.user_field: self.request.user
        }

        serializer = self.get_serializer(data=request.data, many=many_flag)
        serializer.is_valid(raise_exception=True)
        serializer.save(**kwargs)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)


class CountModelMixin(object):
    """
    Count a queryset.
    Cite: https://stackoverflow.com/a/49709157/9708266
    """

    @action(detail=False)
    def count(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        content = {'count': queryset.count()}
        return Response(content)


class PageSizeModelMixin(object):
    """
    Add a page size limit action to viewsets.
    """
    @action(detail=False)
    def pagination_info(self, request, *args, **kwargs):
        """
        Return the maximum page size limit for paginated requests.
        """
        default_page_size = api_settings.PAGE_SIZE
        page_size_limit = settings.REST_FRAMEWORK.get('PAGE_SIZE', None)

        return Response({
            'default_page_size': default_page_size,
            'page_size_limit': page_size_limit})


class ListModelFieldsMixin:
    @action(detail=False, methods=['get'])
    def fields(self, request, *args, **kwargs):
        # Define a dummy serializer class for the model
        # associated with the viewset
        class DummySerializer(ModelSerializer):
            class Meta:
                model = self.queryset.model
                fields = '__all__'

        # Get the _readable_fields attribute of the dummy serializer instance
        readable = [field.source for field in
                           DummySerializer()._readable_fields]
        writeable = [field.source for field in
                            DummySerializer()._writable_fields]

        automatically_generated = ['id',
                                   'uploader',
                                   'uploadDate',
                                   'modified']

        # Return the readable fields as a JSON response
        return Response({"readable": readable,
                         "writeable": writeable,
                         "automatically_generated":
                         automatically_generated},
                        status=status.HTTP_200_OK)


class ChrMapViewSet(ListModelFieldsMixin,
                    CustomCreateMixin,
                    PageSizeModelMixin,
                    viewsets.ModelViewSet,
                    CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ChrMap.objects.all().order_by('id')  # noqa
    serializer_class = ChrMapSerializer  # noqa
    permission_classes = (AllowAny,)

    # def perform_create(self, **kwargs):
    #     super().perform_create(**kwargs)

    # def perform_create(self, serializer):
    #     serializer.save(uploader=self.request.user)


class GeneViewSet(ListModelFieldsMixin,
                  CustomCreateMixin,
                  PageSizeModelMixin,
                  viewsets.ModelViewSet,
                  CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Gene.objects.all().order_by('id')  # noqa
    serializer_class = GeneSerializer  # noqa
    permission_classes = (AllowAny,)


class PromoterRegionsViewSet(ListModelFieldsMixin,
                             CustomCreateMixin,
                             PageSizeModelMixin,
                             viewsets.ModelViewSet,
                             CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = PromoterRegions.objects.all().order_by('id')  # noqa
    serializer_class = PromoterRegionsSerializer  # noqa
    permission_classes = (AllowAny,)


class HarbisonChIPViewSet(ListModelFieldsMixin,
                          CustomCreateMixin,
                          PageSizeModelMixin,
                          viewsets.ModelViewSet,
                          CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HarbisonChIP.objects.all().order_by('id')  # noqa
    serializer_class = HarbisonChIPSerializer  # noqa
    permission_classes = (AllowAny,)


class KemmerenTFKOViewSet(ListModelFieldsMixin,
                          CustomCreateMixin,
                          PageSizeModelMixin,
                          viewsets.ModelViewSet,
                          CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KemmerenTFKO.objects.all().order_by('id')  # noqa
    serializer_class = KemmerenTFKOSerializer  # noqa
    permission_classes = (AllowAny,)


class McIsaacZEVViewSet(ListModelFieldsMixin,
                        CustomCreateMixin,
                        PageSizeModelMixin,
                        viewsets.ModelViewSet,
                        CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = McIsaacZEV.objects.all().order_by('id')  # noqa
    serializer_class = McIsaacZEVSerializer  # noqa
    permission_classes = (AllowAny,)


class BackgroundViewSet(ListModelFieldsMixin,
                        CustomCreateMixin,
                        PageSizeModelMixin,
                        viewsets.ModelViewSet,
                        CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Background.objects.all().order_by('id')  # noqa
    serializer_class = BackgroundSerializer  # noqa
    permission_classes = (AllowAny,)


class CCTFViewSet(ListModelFieldsMixin,
                  CustomCreateMixin,
                  PageSizeModelMixin,
                  viewsets.ModelViewSet,
                  CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CCTF.objects.all().order_by('id')  # noqa
    serializer_class = CCTFSerializer  # noqa
    permission_classes = (AllowAny,)


class CCExperimentViewSet(ListModelFieldsMixin,
                          CustomCreateMixin,
                          PageSizeModelMixin,
                          viewsets.ModelViewSet,
                          CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CCExperiment.objects.all().order_by('id')  # noqa
    serializer_class = CCExperimentSerializer  # noqa
    permission_classes = (AllowAny,)


class HopsViewSet(ListModelFieldsMixin,
                  CustomCreateMixin,
                  PageSizeModelMixin,
                  viewsets.ModelViewSet,
                  CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Hops.objects.all().order_by('id')  # noqa
    serializer_class = HopsSerializer  # noqa
    permission_classes = (AllowAny,)


class HopsReplicacteSigViewSet(ListModelFieldsMixin,
                               CustomCreateMixin,
                               PageSizeModelMixin,
                               viewsets.ModelViewSet,
                               CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HopsReplicateSig.objects.all().order_by('id')  # noqa
    serializer_class = HopsReplicateSigSerializer  # noqa
    permission_classes = (AllowAny,)


class QcMetricsViewSet(ListModelFieldsMixin,
                       CustomCreateMixin,
                       PageSizeModelMixin,
                       viewsets.ModelViewSet,
                       CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcMetrics.objects.all().order_by('id')  # noqa
    serializer_class = QcMetricsSerializer  # noqa
    permission_classes = (AllowAny,)


class QcManualReviewViewSet(ListModelFieldsMixin,
                            CustomCreateMixin,
                            PageSizeModelMixin,
                            viewsets.ModelViewSet,
                            CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcManualReview.objects.all().order_by('id')  # noqa
    serializer_class = QcManualReviewSerializer  # noqa
    permission_classes = (AllowAny,)


class QcR1ToR2ViewSet(ListModelFieldsMixin,
                      CustomCreateMixin,
                      PageSizeModelMixin,
                      viewsets.ModelViewSet,
                      CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcR1ToR2Tf.objects.all().order_by('id')  # noqa
    serializer_class = QcR1ToR2TfSerializer  # noqa
    permission_classes = (AllowAny,)


class QcR2ToR1ViewSet(ListModelFieldsMixin,
                      CustomCreateMixin,
                      PageSizeModelMixin,
                      viewsets.ModelViewSet,
                      CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcR2ToR1Tf.objects.all().order_by('id')  # noqa
    serializer_class = QcR2ToR1TfSerializer  # noqa
    permission_classes = (AllowAny,)


class QcTfToTransposonViewSet(ListModelFieldsMixin,
                              CustomCreateMixin,
                              PageSizeModelMixin,
                              viewsets.ModelViewSet,
                              CountModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QcTfToTransposon.objects.all().order_by('id')  # noqa
    serializer_class = QcTfToTransposonSerializer  # noqa
    permission_classes = (AllowAny,)

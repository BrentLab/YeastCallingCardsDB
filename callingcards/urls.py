from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .users.views import UserViewSet, UserCreateViewSet
from .callingcards.views import (ChrMapViewSet, GeneViewSet,
                                 PromoterRegionsViewSet, HarbisonChIPViewSet,
                                 KemmerenTFKOViewSet,
                                 McIsaacZEVViewSet, BackgroundViewSet,
                                 CCTFViewSet,
                                 CCExperimentViewSet, HopsViewSet,
                                 HopsReplicateSigViewSet,
                                 QcMetricsViewSet, QcManualReviewViewSet,
                                 QcR1ToR2ViewSet,
                                 QcR2ToR1ViewSet, QcTfToTransposonViewSet,
                                 QcR1ToR2TfSummaryViewSet,
                                 QcReviewViewSet, ExpressionViewSetViewSet,
                                 check_task_status)


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)
router.register(r'chrmap', ChrMapViewSet, basename='chrmap')
router.register(r'genes', GeneViewSet, basename='gene')
router.register(r'promoterregions', PromoterRegionsViewSet, basename='promoterregions')
router.register(r'harbisonchip', HarbisonChIPViewSet, basename='harbisonchip')
router.register(r'kemmerentfko', KemmerenTFKOViewSet, basename='kemmerentfko')
router.register(r'mcisaaczev', McIsaacZEVViewSet, basename='mcisaaczev')
router.register(r'background', BackgroundViewSet, basename='background')
router.register(r'cctf', CCTFViewSet, basename='cctf')
router.register(r'ccexperiment', CCExperimentViewSet, basename='ccexperiment')
router.register(r'hops', HopsViewSet, basename='hops')
router.register(r'hopsreplicatesig',
                HopsReplicateSigViewSet,
                basename='hopsreplicatesig')
router.register(r'qcmetrics', QcMetricsViewSet, basename='qcmetrics')
router.register(r'qcmanualreview', QcManualReviewViewSet, basename='qcmanualreview')
router.register(r'qcr1tor2', QcR1ToR2ViewSet, basename='qcr1tor2')
router.register(r'qcr2tor1', QcR2ToR1ViewSet, basename='qcr2tor1')
router.register(r'qctftotransposon', QcTfToTransposonViewSet, basename='qctftotransposon')
router.register(r'qcr1tor2summary', QcR1ToR2TfSummaryViewSet,
                basename='qcr1tor2summary')
router.register(r'qc_review', QcReviewViewSet, basename='qcreview')
router.register(r'expression', ExpressionViewSetViewSet,
                basename='expression')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('check_task_status/<str:task_id>/', check_task_status, name='check_task_status'),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

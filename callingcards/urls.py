from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularSwaggerView,
                                   SpectacularRedocView)

from .users.views import UserViewSet, UserCreateViewSet
from .callingcards.views import (ChrMapViewSet,
                                 GeneViewSet,
                                 PromoterRegionsViewSet,
                                 HarbisonChIPViewSet,
                                 KemmerenTFKOViewSet,
                                 McIsaacZEVViewSet,
                                 BackgroundViewSet,
                                 CCTFViewSet,
                                 CCExperimentViewSet,
                                 HopsSourceViewSet,
                                 Hops_s3ViewSet,
                                 HopsViewSet,
                                 LabViewSet,
                                 QcMetricsViewSet,
                                 QcManualReviewViewSet,
                                 QcR1ToR2ViewSet,
                                 QcR2ToR1ViewSet,
                                 QcTfToTransposonViewSet,
                                 QcR1ToR2TfSummaryViewSet,
                                 QcReviewViewSet,
                                 ExpressionViewSet,
                                 TaskStatusViewSet)


router = DefaultRouter()
router.register(r'users',
                UserViewSet)
router.register(r'users',
                UserCreateViewSet)
router.register(r'chrmap',
                ChrMapViewSet,
                basename='chrmap')
router.register(r'genes',
                GeneViewSet,
                basename='gene')
router.register(r'promoterregions',
                PromoterRegionsViewSet,
                basename='promoterregions')
router.register(r'harbisonchip',
                HarbisonChIPViewSet,
                basename='harbisonchip')
router.register(r'kemmerentfko',
                KemmerenTFKOViewSet,
                basename='kemmerentfko')
router.register(r'mcisaaczev',
                McIsaacZEVViewSet,
                basename='mcisaaczev')
router.register(r'background',
                BackgroundViewSet,
                basename='background')
router.register(r'cctf',
                CCTFViewSet,
                basename='cctf')
router.register(r'ccexperiment',
                CCExperimentViewSet,
                basename='ccexperiment')
router.register(r'hops_source',
                HopsSourceViewSet,
                basename='hopssource')
router.register(r'hops_s3',
                Hops_s3ViewSet,
                basename='hopss3')
router.register(r'lab',
                LabViewSet,
                basename='lab')
router.register(r'hops',
                HopsViewSet,
                basename='hops')
router.register(r'qcmetrics',
                QcMetricsViewSet,
                basename='qcmetrics')
router.register(r'qcmanualreview',
                QcManualReviewViewSet,
                basename='qcmanualreview')
router.register(r'qcr1tor2',
                QcR1ToR2ViewSet,
                basename='qcr1tor2')
router.register(r'qcr2tor1',
                QcR2ToR1ViewSet,
                basename='qcr2tor1')
router.register(r'qctftotransposon',
                QcTfToTransposonViewSet,
                basename='qctftotransposon')
router.register(r'qcr1tor2summary',
                QcR1ToR2TfSummaryViewSet,
                basename='qcr1tor2summary')
router.register(r'qc_review',
                QcReviewViewSet,
                basename='qcreview')
router.register(r'expression',
                ExpressionViewSet,
                basename='expression')
router.register(r'check_task_status',
                TaskStatusViewSet,
                basename='checktaskstatus')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(
        url=reverse_lazy('api-root'), permanent=False)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .users.views import UserViewSet, UserCreateViewSet
from .callingcards.views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)
router.register(r'chrmap', ChrMapViewSet)
router.register(r'genes', GeneViewSet)
router.register(r'promoterregions', PromoterRegionsViewSet)
router.register(r'harbisonchip', HarbisonChIPViewSet)
router.register(r'kemmerentfko', KemmerenTFKOViewSet)
router.register(r'mcisaaczev', McIsaacZEVViewSet)
router.register(r'background', BackgroundViewSet)
router.register(r'cctf', CCTFViewSet)
router.register(r'ccexperiment', CCExperimentViewSet)
router.register(r'hops', HopsViewSet)
router.register(r'hopsreplicatesig', HopsReplicacteSigViewSet)
router.register(r'qcmetrics', QcMetricsViewSet)
router.register(r'qcmanualreview', QcManualReviewViewSet)
router.register(r'qcr1tor2', QcR1ToR2ViewSet)
router.register(r'qcr2tor1', QcR2ToR1ViewSet)
router.register(r'qctftotransposon', QcTfToTransposonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

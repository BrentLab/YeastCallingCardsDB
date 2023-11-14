"""Admin interface for callingcards app."""
from django.contrib import admin  # pylint: disable=E0611,E0401 # noqa # type: ignore
from callingcards.callingcards import models


@admin.register(
    models.Background,
    models.BackgroundSource,
    models.CallingCardsSig,
    models.CCExperiment,
    models.CCTF,
    models.ChrMap,
    models.Gene,
    models.HarbisonChIP,
    models.CallingCards_s3,
    models.Hops,
    models.HopsSource,
    models.KemmerenTFKO,
    models.Lab,
    models.McIsaacZEV,
    models.PromoterRegions,
    models.PromoterRegionsSource,
    models.QcManualReview,
    models.QcMetrics,
    models.QcR1ToR2Tf,
    models.QcR2ToR1Tf,
    models.QcTfToTransposon
)
class CCAdmin(admin.ModelAdmin):
    """cite: https://stackoverflow.com/a/60821878/9708266"""
    pass

"""Admin interface for callingcards app."""
from django.contrib import admin #pylint: disable=E0611,E0401 # noqa # type: ignore
from django.contrib.auth.admin import ModelAdmin #pylint: disable=E0611,E0401 # noqa # type: ignore
from .models import * #pylint: disable=W0401,W0614 # noqa


@admin.register(ChrMap, Gene, PromoterRegions, HarbisonChIP, KemmerenTFKO,  # noqa
                McIsaacZEV, Background, CCTF, CCExperiment, Hops, HopsReplicateSig,  # noqa
                QcAlignment, QcHops, QcManualReview, QcR1ToR2Tf, QcR2ToR1Tf,  # noqa
                QcTfToTransposon)  # noqa
class CCAdmin(ModelAdmin):
    """cite: https://stackoverflow.com/a/60821878/9708266"""
    pass

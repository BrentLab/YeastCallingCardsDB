# pylint: disable=missing-docstring
from enum import Enum
import logging

from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.core.validators import MinValueValidator, MaxValueValidator  # pylint: disable=import-error # noqa # type: ignore
from django.conf import settings  # pylint: disable=import-error # noqa # type: ignore

logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = ['ChrMap', 'Gene', 'PromoterRegions', 'HarbisonChIP', 'KemmerenTFKO',
           'McIsaacZEV', 'Background', 'CCTF', 'CCExperiment', 'Hops',
           'HopsReplicateSig', 'QcAlignment', 'QcHops', 'QcManualReview',
           'QcR1ToR2Tf', 'QcR2ToR1Tf', 'QcTfToTransposon']

class Strand(Enum):
    POSITIVE = '+'
    NEGATIVE = '-'
    UNSTRANDED = '*'


STRAND_CHOICES = ((Strand.POSITIVE.value, '+'),
                  (Strand.NEGATIVE.value, '-'),
                  (Strand.UNSTRANDED.value, '*'))

class BaseModel(models.Model):
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                 related_name='capsule_image_uploader', 
                                 on_delete=models.PROTECT)
    uploadDate = models.DateField(auto_now_add=True)
    # record when the record is modified
    # note: this only updates with model.save(), not queryset.update
    #       see docs -- may need to write some code to update this field 
    #       for update statement when only certain fields are changed?
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ChrMap(BaseModel):
    refseq = models.CharField(
        max_length=10)
    igenomes = models.CharField(
        max_length=10)
    ensembl = models.CharField(
        max_length=10)
    ucsc = models.CharField(
        max_length=10)
    mitra = models.CharField(
        max_length=10)
    seqlength = models.PositiveIntegerField()
    numbered = models.PositiveSmallIntegerField()
    chr = models.CharField(
        max_length=10)

    class Meta:
        managed = True
        db_table = 'chr_map'


class Gene(BaseModel):

    chr = models.ForeignKey(
        'ChrMap',
        models.PROTECT,
        blank=True,
        null=True)
    start = models.PositiveIntegerField()
    # TODO put constraint on end cannot be past end of chr
    end = models.IntegerField()
    strand = models.Charfield(
        max_length=1,
        choices=STRAND_CHOICES,
        default=Strand.UNSTRANDED.value)
    feature_ontology = models.CharField(
        blank=True,
        null=True)
    biotype = models.CharField(
        blank=True,
        null=True)
    systematic = models.CharField(
        unique=True,
        max_length=20)
    name = models.CharField(
        max_length=20)
    source = models.CharField(
        max_length=20)
    alias = models.CharField(
        max_length=20)
    tf = models.BooleanField(
        default=False)


class PromoterRegions(BaseModel):
    chr = models.ForeignKey(
        'chr_map',
        models.PROTECT)
    start = models.IntegerField()
    # TODO put constraint on end cannot be past end of chr
    end = models.IntegerField()
    strand = models.Charfield(
        max_length=1,
        choices=STRAND_CHOICES,
        default=Strand.UNSTRANDED.value)
    associated_feature = models.ForeignKey(
        'gene',
        models.PROTECT)
    score = models.PositiveSmallIntegerField(
        default=100,
        validators=[MaxValueValidator(100)]
    )

    class Meta:
        managed = True
        db_table = 'Regions'


class HarbisonChIP(BaseModel):
    CHIP_CHIP = 'chip_chip'
    CHIP_EXO = 'chip_exo'

    TYPE_CHOICES = ((CHIP_CHIP, 'chip_chip'),
                    (CHIP_EXO, 'chip_exo'))

    gene = models.ForeignKey(
        'gene',
        models.PROTECT)
    effect = models.FloatField(
        null=True)
    pval = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    tf = models.ForeignKey(
        'gene',
        models.PROTECT)
    type = models.CharField(
        choices=TYPE_CHOICES)
    source = models.CharField(
        max_length=50)

    class Meta:
        managed = True
        db_table = 'harbison_chip'


class KemmerenTFKO(BaseModel):
    gene = models.ForeignKey(
        'gene',
        models.PROTECT)
    effect = models.FloatField()
    padj = models.FloatField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    tf = models.CharField(blank=True, null=True)
    source = models.CharField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'kemmeren_tfko'


class McIsaacZEV(BaseModel):
    gene = models.ForeignKey(
        'gene',
        models.PROTECT)
    effect = models.FloatField()
    tf = models.CharField(blank=True, null=True)
    source = models.CharField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'mcisaac_zev'


class Background(BaseModel):
    DSIR4 = 'dsir4'
    ADH1 = 'adh1'

    SOURCE_CHOICES = ((DSIR4, 'dsir4'),
                      (ADH1, 'adh1'))

    chr = models.ForeignKey(
        'ChrMap', models.PROTECT)
    start = models.IntegerField()
    # TODO put constraint on end cannot be past end of chr
    end = models.IntegerField()
    strand = models.Charfield(
        max_length=1,
        choices=STRAND_CHOICES,
        default=Strand.UNSTRANDED.value)
    depth = models.PositiveIntegerField()
    source = models.CharField(
        choices=SOURCE_CHOICES)

    class Meta:
        managed = True
        db_table = 'background'


class CCTF(BaseModel):
    """this table is used to store a list of the transcription factors
     interrogated with calling cards"""
    tf = models.ForeignKey(
        'gene',
        models.PROTECT)
    strain = models.CharField(
        max_length=20,
        default='unknown'
    )
    under_development = models.BooleanField(
        default=False)
    notes = models.CharField(
        max_length=50,
        default='none'
    )

    class Meta:
        managed = True
        db_table = 'cc_tf'

class CCExperiment(BaseModel):
    """this table is used to keep a record of the batches (most likely runs)
     in which a given set of transcription factors were interrogated with 
     calling cards"""
    # likely a run number, eg run_1234
    batch = models.CharField()
    # id of a record in the gene table
    tf = models.ForeignKey(
        'cc_tf',
        models.CASCADE)
    # when the same tf is used in multiple experiments, each sample should be
    # uniquely identified by batch_replicate
    batch_replicate = models.PositiveSmallIntegerField(
        default=1
    )

    class Meta:
        managed = True
        db_table = 'cc_experiment'


class Hops(BaseModel):
    chr = models.foreignKey(
        'chr_map',
        models.PROTECT)
    start = models.IntegerField()
    # TODO put constraint on end cannot be past end of chr
    end = models.IntegerField()
    strand = models.Charfield(
        max_length=1,
        choices=STRAND_CHOICES,
        default=Strand.UNSTRANDED.value)
    depth = models.PositiveIntegerField()
    experiment = models.ForeignKey(
        'cc_experiment',
        models.CASCADE)

    class Meta:
        managed = True
        db_table = 'hops'


class HopsReplicateSig(BaseModel):
    """Significance of a HOPS peak in single replicate for a given background and promoter region definition """
    chr = models.foreignKey(
        'chr_map',
        models.PROTECT)
    start = models.IntegerField()
    # TODO put constraint on end cannot be past end of chr
    end = models.IntegerField()
    strand = models.Charfield(
        max_length=1,
        choices=STRAND_CHOICES,
        default=Strand.UNSTRANDED.value)
    bg_hops = models.PositiveIntegerField()
    expr_hops = models.PositiveIntegerField()
    experiment = models.ForeignKey(
        'cc_experiment',
        models.CASCADE)
    poisson_pval = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    hypergeom_pval = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    background = models.CharField(
        max_length=10,
        choices=Background.SOURCE_CHOICES
    )
    promoter_regions = models.CharField(
        max_length=20,
        choices=PromoterRegions.TYPE_CHOICES
    )

    class Meta:
        managed = True
        db_table = 'hops_replicate_sig'


class QcAlignment(BaseModel):
    experiment = models.ForeignKey(Batch, models.DO_NOTHING, blank=True, null=True)
    total_reads = models.IntegerField(blank=True, null=True)
    hpaii = models.IntegerField(blank=True, null=True)
    hinp1i = models.IntegerField(blank=True, null=True)
    taqai = models.IntegerField(blank=True, null=True)
    undet = models.IntegerField(blank=True, null=True)
    genome_mapped = models.IntegerField(blank=True, null=True)
    plasmid_mapped = models.IntegerField(blank=True, null=True)
    unmapped = models.IntegerField(blank=True, null=True)
    multimapped = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'qc_alignment'


class QcHops(BaseModel):
    batch = models.ForeignKey(Batch, models.DO_NOTHING, blank=True, null=True)
    total = models.IntegerField()
    transpositions = models.IntegerField()
    plasmid_transpositions = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qc_hops'


class QcManualReview(BaseModel):
    batch = models.ForeignKey(Batch, models.DO_NOTHING, blank=True, null=True)
    rank_recall = models.CharField(blank=True, null=True)
    chip_better = models.CharField(blank=True, null=True)
    data_usable = models.CharField(blank=True, null=True)
    passing_replicate = models.CharField(blank=True, null=True)
    notes = models.CharField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'qc_manual_review'


class QcR1ToR2Tf(BaseModel):
    batch = models.ForeignKey(Batch, models.DO_NOTHING, blank=True, null=True)
    edit_dist = models.IntegerField()
    tally = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qc_r1_to_r2_tf'


class QcR2ToR1Tf(BaseModel):
    batch = models.ForeignKey(Batch, models.DO_NOTHING, blank=True, null=True)
    edit_dist = models.IntegerField()
    tally = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qc_r2_to_r1_tf'


class QcTfToTransposon(BaseModel):
    batch = models.ForeignKey(Batch, models.DO_NOTHING, blank=True, null=True)
    edit_dist = models.IntegerField()
    tally = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qc_tf_to_transposon'

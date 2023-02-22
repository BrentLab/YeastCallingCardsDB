# pylint: disable=missing-docstring
from enum import Enum
import logging

from django.db import models  # pylint: disable=import-error # noqa # type: ignore
from django.core.validators import MinValueValidator, MaxValueValidator  # pylint: disable=import-error # noqa # type: ignore
from django.conf import settings  # pylint: disable=import-error # noqa # type: ignore

logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = ['ChrMap', 'Gene', 'PromoterRegions', 'HarbisonChIP', 'KemmerenTFKO',
           'McIsaacZEV', 'Background', 'CCTF', 'CCExperiment', 'Hops',
           'HopsReplicateSig', 'QcMetrics', 'QcManualReview',
           'QcR1ToR2Tf', 'QcR2ToR1Tf', 'QcTfToTransposon']

class Strand(Enum):
    POSITIVE = '+'
    NEGATIVE = '-'
    UNSTRANDED = '*'


STRAND_CHOICES = ((Strand.POSITIVE.value, '+'),
                  (Strand.NEGATIVE.value, '-'),
                  (Strand.UNSTRANDED.value, '*'))

class BaseModel(models.Model):
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
        max_length=12)
    igenomes = models.CharField(
        max_length=6)
    ensembl = models.CharField(
        max_length=6)
    ucsc = models.CharField(
        max_length=8)
    mitra = models.CharField(
        max_length=15)
    seqlength = models.PositiveIntegerField()
    numbered = models.PositiveSmallIntegerField()
    chr = models.CharField(
        max_length=6)

    class Meta:
        managed = True
        db_table = 'chr_map'


class Gene(BaseModel):

    chr = models.ForeignKey(
        'ChrMap',
        models.PROTECT)
    start = models.PositiveIntegerField()
    # TODO put constraint on end cannot be past end of chr
    end = models.IntegerField()
    strand = models.CharField(
        max_length=1,
        choices=STRAND_CHOICES,
        default=Strand.UNSTRANDED.value)
    feature_ontology = models.CharField(
        max_length=20,
        default='unknown'
    )
    biotype = models.CharField(
        max_length=20,
        default='unknown'
    )
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

    NOT_ORF = 'not_orf'
    YIMING = 'yiming'

    SOURCE_CHOICES = ((NOT_ORF, 'not_orf'),
                      (YIMING, 'yiming'))

    chr = models.ForeignKey(
        'ChrMap',
        models.PROTECT)
    start = models.IntegerField()
    # TODO put constraint on end cannot be past end of chr
    end = models.IntegerField()
    strand = models.CharField(
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
    source = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES
    )

    class Meta:
        managed = True
        db_table = 'promoter_regions'


class HarbisonChIP(BaseModel):

    gene = models.ForeignKey(
        'Gene',
        models.PROTECT)
    effect = models.FloatField()
    pval = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    tf = models.ForeignKey(
        'Gene',
        models.PROTECT)

    class Meta:
        managed = True
        db_table = 'harbison_chip'


class KemmerenTFKO(BaseModel):
    gene = models.ForeignKey(
        'Gene',
        models.PROTECT)
    effect = models.FloatField()
    padj = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)])
    tf = models.ForeignKey(
        'Gene',
        models.PROTECT)

    class Meta:
        managed = True
        db_table = 'kemmeren_tfko'


class McIsaacZEV(BaseModel):
    gene = models.ForeignKey(
        'Gene',
        models.PROTECT)
    effect = models.FloatField()
    tf = models.ForeignKey(
        'Gene',
        models.PROTECT)

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
    strand = models.CharField(
        max_length=1,
        choices=STRAND_CHOICES,
        default=Strand.UNSTRANDED.value)
    depth = models.PositiveIntegerField()
    source = models.CharField(
        max_length=5,
        choices=SOURCE_CHOICES)

    class Meta:
        managed = True
        db_table = 'background'


class CCTF(BaseModel):
    """this table is used to store a list of the transcription factors
     interrogated with calling cards"""
    tf = models.ForeignKey(
        'Gene',
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
    batch = models.CharField(
        max_length=15
    )
    # id of a record in the gene table
    tf = models.ForeignKey(
        'CCTF',
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
    chr = models.ForeignKey(
        'ChrMap',
        models.PROTECT)
    start = models.IntegerField()
    # TODO put constraint on end cannot be past end of chr
    end = models.IntegerField()
    strand = models.CharField(
        max_length=1,
        choices=STRAND_CHOICES,
        default=Strand.UNSTRANDED.value)
    depth = models.PositiveIntegerField()
    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE)

    class Meta:
        managed = True
        db_table = 'hops'


class HopsReplicateSig(BaseModel):
    """Significance of a HOPS peak in single replicate for a given
     background and promoter region definition"""
    
    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE)
    chr = models.ForeignKey(
        'ChrMap',
        models.PROTECT)
    start = models.IntegerField()
    # TODO put constraint on end cannot be past end of chr
    end = models.IntegerField()
    strand = models.CharField(
        max_length=1,
        choices=STRAND_CHOICES,
        default=Strand.UNSTRANDED.value)
    bg_hops = models.PositiveIntegerField()
    expr_hops = models.PositiveIntegerField()
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
    promoters = models.CharField(
        max_length=20,
        choices=PromoterRegions.SOURCE_CHOICES
    )

    class Meta:
        managed = True
        db_table = 'hops_replicate_sig'


class QcMetrics(BaseModel):
    
    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE)
    total_aligned = models.PositiveIntegerField()
    unmapped = models.PositiveIntegerField()
    multimapped = models.PositiveIntegerField()
    genome_mapped = models.PositiveIntegerField()
    plasmid_mapped = models.PositiveIntegerField()
    # note the sum of the hops is total hops
    genome_hops = models.PositiveIntegerField()
    plasmid_hops = models.PositiveIntegerField()
    hpaii = models.PositiveIntegerField()
    hinp1i = models.PositiveIntegerField()
    taqai = models.PositiveIntegerField()
    undet = models.PositiveIntegerField()

    class Meta:
        managed = True
        db_table = 'qc_alignment'

class QcManualReview(BaseModel):

    PASS = 'pass'
    FAIL = 'fail'

    YES = 'yes'
    NO = 'no'

    UNREVIEWED = 'unreviewed'

    PASS_FAIL = ((PASS, 'pass'),
                 (FAIL, 'fail'),
                 (UNREVIEWED, 'unreviewed'))

    YES_NO = ((YES, 'yes'),
              (NO, 'no'),
              (UNREVIEWED, 'unreviewed'))

    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE)
    rank_recall = models.CharField(
        max_length=10,
        choices=PASS_FAIL,
        default=UNREVIEWED)
    chip_better = models.CharField(
        max_length=10,
        choices=YES_NO,
        default=UNREVIEWED)
    data_usable = models.CharField(
        max_length=10,
        choices=YES_NO,
        default=UNREVIEWED)
    passing_replicate = models.CharField(
        max_length=10,
        choices=YES_NO,
        default=UNREVIEWED)
    notes = models.CharField(
        max_length=100,
        default='none'
    )

    class Meta:
        managed = True
        db_table = 'qc_manual_review'


class QcR1ToR2Tf(BaseModel):
    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE)
    edit_dist = models.PositiveSmallIntegerField()
    tally = models.PositiveSmallIntegerField()

    class Meta:
        managed = True
        db_table = 'qc_r1_to_r2_tf'


class QcR2ToR1Tf(BaseModel):
    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE)
    edit_dist = models.IntegerField()
    tally = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qc_r2_to_r1_tf'


class QcTfToTransposon(BaseModel):
    experiment = models.ForeignKey(
        'CCExperiment',
        models.CASCADE)
    edit_dist = models.IntegerField()
    tally = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'qc_tf_to_transposon'

# """models for the callingcards app"""

# # pylint: disable=missing-docstring
# from enum import Enum
# import logging

# from django.db import models  # pylint: disable=import-error # noqa # type: ignore
# from django.core.validators import MinValueValidator, MaxValueValidator  # pylint: disable=import-error # noqa # type: ignore
# from django.conf import settings  # pylint: disable=import-error # noqa # type: ignore

# from .querysets import (HopsReplicateSigQuerySet, 
#                         PromoterRegionsQuerySet,
#                         HarbisonChIPQuerySet,
#                         CCTFQuerySet)

# logging.getLogger(__name__).addHandler(logging.NullHandler())

# # eg 0.0000010400103010033001040302
# P_VAL_MAX_DIGITS = 29
# P_VAL_DECIMAL_PLACES = 28

# # eg 99999.0000010400103010033001040302
# EFFECT_MAX_DIGITS = 33
# EFFECT_DECIMAL_PLACES = 28

# class Strand(Enum):
#     POSITIVE = '+'
#     NEGATIVE = '-'
#     UNSTRANDED = '*'


# STRAND_CHOICES = ((Strand.POSITIVE.value, '+'),
#                   (Strand.NEGATIVE.value, '-'),
#                   (Strand.UNSTRANDED.value, '*'))


# class BaseModel(models.Model):
#     uploader = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.PROTECT)
#     uploadDate = models.DateField(auto_now_add=True)
#     # record when the record is modified
#     # note: this only updates with model.save(), not queryset.update
#     #       see docs -- may need to write some code to update this field
#     #       for update statement when only certain fields are changed?
#     modified = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True

# class GenonomicCoordinatesMixin(models.Model):
#     class Meta:
#         abstract = True
#         constraints = [
#             models.CheckConstraint(
#                 check=models.Q(end__lte=models.F('chr__seqlength')),
#                 name='end_cannot_exceed_chromosome_length',
#             )
#         ]


# class ChrMap(BaseModel):
#     """
#     ChrMap model represents chromosome mapping information, including various
#     IDs and names used in different genome databases and the chromosome's 
#     length.

#     Fields:
#         refseq (CharField): RefSeq ID for the chromosome.
#         igenomes (CharField): iGenomes ID for the chromosome.
#         ensembl (CharField): Ensembl ID for the chromosome.
#         ucsc (CharField): UCSC ID for the chromosome.
#         mitra (CharField): Mitra ID for the chromosome.
#         seqlength (PositiveIntegerField): Length of the chromosome sequence.
#         numbered (CharField): Numbered name for the chromosome.
#         chr (CharField): Chromosome name.
#     """
#     refseq = models.CharField(
#         max_length=12)
#     igenomes = models.CharField(
#         max_length=12)
#     ensembl = models.CharField(
#         max_length=12)
#     ucsc = models.CharField(
#         max_length=12)
#     mitra = models.CharField(
#         max_length=15)
#     seqlength = models.PositiveIntegerField()
#     numbered = models.CharField(
#         max_length=12
#     )
#     chr = models.CharField(
#         max_length=12)

#     class Meta:
#         managed = True
#         db_table = 'chr_map'

# class Gene(GenonomicCoordinatesMixin, BaseModel):

#     chr = models.ForeignKey(
#         'ChrMap',
#         models.PROTECT,
#         db_index=True)
#     start = models.PositiveIntegerField()
#     end = models.IntegerField()
#     strand = models.CharField(
#         max_length=1,
#         choices=STRAND_CHOICES,
#         default=Strand.UNSTRANDED.value)
#     type = models.CharField(
#         max_length=30,
#         default='unknown'
#     )
#     gene_biotype = models.CharField(
#         max_length=20,
#         default='unknown'
#     )
#     # note: in the save method below, a unique integer is appended to the
#     # default value if the this field is left blank on input
#     locus_tag = models.CharField(
#         unique=True,
#         max_length=20,
#         default='unknown')
#     # note: in the save method below, a unique integer is appended to the
#     # default value if the this field is left blank on input
#     gene = models.CharField(
#         max_length=20,
#         default='unknown')
#     source = models.CharField(
#         max_length=50)
#     # note: in the save method below, a unique integer is appended to the
#     # default value if the this field is left blank on input
#     alias = models.CharField(
#         max_length=150,
#         default='unknown')
#     note = models.CharField(
#         max_length=1000,
#         default='none')

#     def save(self, *args, **kwargs):

#         # Get the maximum value of the auto-incremented field in the table
#         max_id = Gene.objects.aggregate(models.Max('id'))['id__max'] or 0
#         # Check if the systematic field has the default value
#         if self.locus_tag == 'unknown':
#             self.locus_tag = f'unknown_{max_id + 1}'

#         if self.gene == 'unknown':
#             self.gene = f'unknown_{max_id + 1}'

#         if self.alias == 'unknown':
#             self.alias = f'unknown_{max_id + 1}'

#         super().save(*args, **kwargs)

#     class Meta:
#         managed = True
#         db_table = 'gene'


# class PromoterRegions(GenonomicCoordinatesMixin,
#                       BaseModel):

#     objects = PromoterRegionsQuerySet.as_manager()

#     NOT_ORF = 'not_orf'
#     YIMING = 'yiming'

#     SOURCE_CHOICES = ((NOT_ORF, 'not_orf'),
#                       (YIMING, 'yiming'))

#     chr = models.ForeignKey(
#         'ChrMap',
#         models.PROTECT,
#         db_index=True)
#     start = models.PositiveBigIntegerField()
#     end = models.IntegerField()
#     strand = models.CharField(
#         max_length=1,
#         choices=STRAND_CHOICES,
#         default=Strand.UNSTRANDED.value)
#     associated_feature = models.ForeignKey(
#         'gene',
#         models.PROTECT,
#         db_index=True,
#         related_name='genepromoter')
#     associated_direction = models.CharField(
#         max_length=1,
#         choices=STRAND_CHOICES,
#         default=Strand.UNSTRANDED.value
#     )
#     score = models.PositiveSmallIntegerField(
#         default=100,
#         validators=[MaxValueValidator(100)]
#     )
#     source = models.CharField(
#         max_length=10,
#         choices=SOURCE_CHOICES
#     )

#     class Meta:
#         managed = True
#         db_table = 'promoter_regions'


# class HarbisonChIP(BaseModel):

#     objects = HarbisonChIPQuerySet.as_manager()

#     # note that foreignkey fields automatically
#     # create an index on the field
#     gene = models.ForeignKey(
#         'Gene',
#         models.PROTECT,
#         related_name='harbisonchip_target',
#         db_index=True)
#     tf = models.ForeignKey(
#         'Gene',
#         models.PROTECT,
#         related_name='harbisonchip_tf',
#         db_index=True)
#     pval = models.DecimalField(
#         validators=[MinValueValidator(0), MaxValueValidator(1)],
#         max_digits=P_VAL_MAX_DIGITS,
#         decimal_places=P_VAL_DECIMAL_PLACES
#     )

#     class Meta:
#         managed = True
#         db_table = 'harbison_chip'


# class KemmerenTFKO(BaseModel):
#     gene = models.ForeignKey(
#         'Gene',
#         models.PROTECT,
#         related_name='kemmerentfko_target')
#     effect = models.DecimalField(
#         max_digits=EFFECT_MAX_DIGITS,
#         decimal_places=EFFECT_DECIMAL_PLACES
#     )
#     padj = models.DecimalField(
#         validators=[MinValueValidator(0), MaxValueValidator(1)],
#         max_digits=P_VAL_MAX_DIGITS,
#         decimal_places=P_VAL_DECIMAL_PLACES)
#     tf = models.ForeignKey(
#         'Gene',
#         models.PROTECT,
#         related_name='kemmerentfko_tf',
#         db_index=True)

#     class Meta:
#         managed = True
#         db_table = 'kemmeren_tfko'


# class McIsaacZEV(BaseModel):
#     gene = models.ForeignKey(
#         'Gene',
#         models.PROTECT,
#         related_name='mcisaaczev_target')
#     effect = models.DecimalField(
#         max_digits=EFFECT_MAX_DIGITS,
#         decimal_places=EFFECT_DECIMAL_PLACES
#     )
#     pval = models.DecimalField(
#         validators=[MinValueValidator(0), MaxValueValidator(1)],
#         default=0.0,
#         null=False,
#         max_digits=P_VAL_MAX_DIGITS,
#         decimal_places=P_VAL_DECIMAL_PLACES)
#     tf = models.ForeignKey(
#         'Gene',
#         models.PROTECT,
#         related_name='mcisaaczev_tf',
#         db_index=True)

#     class Meta:
#         managed = True
#         db_table = 'mcisaac_zev'


# class Background(BaseModel):
#     DSIR4 = 'dsir4'
#     ADH1 = 'adh1'

#     SOURCE_CHOICES = ((DSIR4, 'dsir4'),
#                       (ADH1, 'adh1'))

#     chr = models.ForeignKey(
#         'ChrMap', models.PROTECT,
#         db_index=True)
#     start = models.IntegerField()
#     # TODO put constraint on end cannot be past end of chr
#     end = models.IntegerField()
#     strand = models.CharField(
#         max_length=1,
#         choices=STRAND_CHOICES,
#         default=Strand.UNSTRANDED.value)
#     depth = models.PositiveIntegerField()
#     source = models.CharField(
#         max_length=5,
#         choices=SOURCE_CHOICES)

#     class Meta:
#         managed = True
#         db_table = 'background'


# class CCTF(BaseModel):
#     """this table is used to store a list of the transcription factors
#      interrogated with calling cards"""
    
#     objects = CCTFQuerySet.as_manager()

#     tf = models.ForeignKey(
#         'Gene',
#         models.PROTECT,
#         db_index=True)
#     strain = models.CharField(
#         max_length=20,
#         default='unknown'
#     )
#     under_development = models.BooleanField(
#         default=False)
#     notes = models.CharField(
#         max_length=50,
#         default='none'
#     )

#     class Meta:
#         managed = True
#         db_table = 'cc_tf'


# class CCExperiment(BaseModel):
#     """this table is used to keep a record of the batches (most likely runs)
#      in which a given set of transcription factors were interrogated with 
#      calling cards"""
#     # likely a run number, eg run_1234
#     batch = models.CharField(
#         max_length=15
#     )
#     # id of a record in the gene table
#     tf = models.ForeignKey(
#         'CCTF',
#         models.CASCADE,
#         db_index=True)
#     # when the same tf is used in multiple experiments, each sample should be
#     # uniquely identified by batch_replicate
#     batch_replicate = models.PositiveSmallIntegerField(
#         default=1
#     )

#     class Meta:
#         managed = True
#         db_table = 'cc_experiment'


# class Hops(BaseModel):
#     chr = models.ForeignKey(
#         'ChrMap',
#         models.PROTECT,
#         db_index=True)
#     start = models.IntegerField()
#     # TODO put constraint on end cannot be past end of chr
#     end = models.IntegerField()
#     strand = models.CharField(
#         max_length=1,
#         choices=STRAND_CHOICES,
#         default=Strand.UNSTRANDED.value)
#     depth = models.PositiveIntegerField()
#     experiment = models.ForeignKey(
#         'CCExperiment',
#         models.CASCADE,
#         db_index=True)

#     class Meta:
#         managed = True
#         db_table = 'hops'


# class HopsReplicateSig(BaseModel):
#     """Significance of a HOPS peak in single replicate for a given
#      background and promoter region definition"""

#     objects = HopsReplicateSigQuerySet.as_manager()

#     experiment = models.ForeignKey(
#         'CCExperiment',
#         models.CASCADE,
#         db_index=True)
#     promoter = models.ForeignKey(
#         'PromoterRegions',
#         models.PROTECT,
#         db_index=True)
#     bg_hops = models.PositiveIntegerField()
#     expr_hops = models.PositiveIntegerField()
#     effect = models.DecimalField(
#         max_digits=EFFECT_MAX_DIGITS,
#         decimal_places=EFFECT_DECIMAL_PLACES)
#     poisson_pval = models.DecimalField(
#         validators=[MinValueValidator(0), MaxValueValidator(1)],
#         max_digits=P_VAL_MAX_DIGITS,
#         decimal_places=P_VAL_DECIMAL_PLACES
#     )
#     hypergeom_pval = models.DecimalField(
#         validators=[MinValueValidator(0), MaxValueValidator(1)],
#         max_digits=P_VAL_MAX_DIGITS,
#         decimal_places=P_VAL_DECIMAL_PLACES
#     )
#     background = models.CharField(
#         max_length=10,
#         choices=Background.SOURCE_CHOICES
#     )

#     class Meta:
#         managed = True
#         db_table = 'hops_replicate_sig'


# class QcMetrics(BaseModel):

#     experiment = models.ForeignKey(
#         'CCExperiment',
#         models.CASCADE,
#         db_index=True)
#     total_reads = models.PositiveIntegerField()
#     unmapped = models.PositiveIntegerField()
#     multimapped = models.PositiveIntegerField()
#     genome_mapped = models.PositiveIntegerField()
#     plasmid_mapped = models.IntegerField(
#         validators=[MinValueValidator(-1)]
#     )
#     hpaii = models.PositiveIntegerField()
#     hinp1i = models.PositiveIntegerField()
#     taqai = models.PositiveIntegerField()
#     undet = models.PositiveIntegerField()
#     note = models.CharField(
#         max_length=50,
#         default='none'
#     )

#     class Meta:
#         managed = True
#         db_table = 'qc_alignment'

# class QcManualReview(BaseModel):

#     PASS = 'pass'
#     FAIL = 'fail'

#     YES = 'yes'
#     NO = 'no'
#     NOTE = 'note'

#     UNREVIEWED = 'unreviewed'

#     PASS_FAIL = ((PASS, 'pass'),
#                  (FAIL, 'fail'),
#                  (UNREVIEWED, 'unreviewed'),
#                  (NOTE, 'note'))

#     YES_NO = ((YES, 'yes'),
#               (NO, 'no'),
#               (UNREVIEWED, 'unreviewed'),
#               (NOTE, 'note'))

#     experiment = models.ForeignKey(
#         'CCExperiment',
#         models.CASCADE,
#         db_index=True)
#     rank_recall = models.CharField(
#         max_length=10,
#         choices=PASS_FAIL,
#         default=UNREVIEWED)
#     chip_better = models.CharField(
#         max_length=10,
#         choices=YES_NO,
#         default=UNREVIEWED)
#     data_usable = models.CharField(
#         max_length=10,
#         choices=YES_NO,
#         default=UNREVIEWED)
#     passing_replicate = models.CharField(
#         max_length=10,
#         choices=YES_NO,
#         default=UNREVIEWED)
#     note = models.CharField(
#         max_length=100,
#         default='none'
#     )

#     class Meta:
#         managed = True
#         db_table = 'qc_manual_review'


# class QcR1ToR2Tf(BaseModel):
#     experiment = models.ForeignKey(
#         'CCExperiment',
#         models.CASCADE,
#         db_index=True)
#     edit_dist = models.PositiveSmallIntegerField()
#     tally = models.IntegerField(
#         validators=[MinValueValidator(-1)]
#     )
#     note = models.CharField(
#         max_length=100,
#         default='none'
#     )

#     class Meta:
#         managed = True
#         db_table = 'qc_r1_to_r2_tf'


# class QcR2ToR1Tf(BaseModel):
#     experiment = models.ForeignKey(
#         'CCExperiment',
#         models.CASCADE,
#         db_index=True)
#     edit_dist = models.IntegerField()
#     tally = models.IntegerField(
#         validators=[MinValueValidator(-1)]
#     )
#     note = models.CharField(
#         max_length=100,
#         default='none'
#     )

#     class Meta:
#         managed = True
#         db_table = 'qc_r2_to_r1_tf'


# class QcTfToTransposon(BaseModel):
#     experiment = models.ForeignKey(
#         'CCExperiment',
#         models.CASCADE,
#         db_index=True)
#     edit_dist = models.IntegerField()
#     tally = models.IntegerField(
#         validators=[MinValueValidator(-1)]
#     )
#     note = models.CharField(
#         max_length=100,
#         default='none'
#     )

#     class Meta:
#         managed = True
#         db_table = 'qc_tf_to_transposon'

# Generated by Django 4.2 on 2023-04-24 22:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('callingcards', '0002_alter_qcr1tor2tf_tally_alter_qcr2tor1tf_tally_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promoterregions',
            name='associated_direction',
        ),
        migrations.AddField(
            model_name='background',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ccexperiment',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cctf',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chrmap',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gene',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='harbisonchip',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hops',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hopsreplicatesig',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='kemmerentfko',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mcisaaczev',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='promoterregions',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='qcmanualreview',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='qcmetrics',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='qcr1tor2tf',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='qcr2tor1tf',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='qctftotransposon',
            name='modifiedBy',
            field=models.ForeignKey(default='86c03f8f-b280-42c2-a5ee-7baffde4790b', on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='background',
            name='end',
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='background',
            name='source',
            field=models.CharField(choices=[('dsir4', 'dsir4'), ('adh1', 'adh1')], db_index=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='background',
            name='start',
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='background',
            name='strand',
            field=models.CharField(choices=[('+', '+'), ('-', '-'), ('*', '*')], db_index=True, default='*', max_length=1),
        ),
        migrations.AlterField(
            model_name='background',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ccexperiment',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cctf',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='chrmap',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gene',
            name='end',
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='gene',
            name='start',
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='gene',
            name='strand',
            field=models.CharField(choices=[('+', '+'), ('-', '-'), ('*', '*')], db_index=True, default='*', max_length=1),
        ),
        migrations.AlterField(
            model_name='gene',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='harbisonchip',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hops',
            name='end',
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='hops',
            name='start',
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='hops',
            name='strand',
            field=models.CharField(choices=[('+', '+'), ('-', '-'), ('*', '*')], db_index=True, default='*', max_length=1),
        ),
        migrations.AlterField(
            model_name='hops',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hopsreplicatesig',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='kemmerentfko',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mcisaaczev',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='promoterregions',
            name='end',
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='promoterregions',
            name='source',
            field=models.CharField(choices=[('not_orf', 'not_orf'), ('yiming', 'yiming')], db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='promoterregions',
            name='start',
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='promoterregions',
            name='strand',
            field=models.CharField(choices=[('+', '+'), ('-', '-'), ('*', '*')], db_index=True, default='*', max_length=1),
        ),
        migrations.AlterField(
            model_name='promoterregions',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='qcmanualreview',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='qcmetrics',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='qcr1tor2tf',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='qcr2tor1tf',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='qctftotransposon',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL),
        ),
    ]

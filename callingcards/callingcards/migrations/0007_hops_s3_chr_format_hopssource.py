# Generated by Django 4.2 on 2023-05-09 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('callingcards', '0006_hops_s3'),
    ]

    operations = [
        migrations.AddField(
            model_name='hops_s3',
            name='chr_format',
            field=models.CharField(choices=[('id', 'id'), ('refseq', 'refseq'), ('igenomes', 'igenomes'), ('ensembl', 'ensembl'), ('ucsc', 'ucsc'), ('mitra', 'mitra'), ('numbered', 'numbered'), ('chr', 'chr')], default='id', max_length=25),
        ),
        migrations.CreateModel(
            name='HopsSource',
            fields=[
                ('uploadDate', models.DateField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('source', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('providence', models.CharField(default='none', max_length=100)),
                ('notes', models.CharField(default='none', max_length=500)),
                ('modifiedBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL)),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'HopsSource',
                'db_table': 'hopssource',
                'ordering': ['source'],
                'managed': True,
            },
        ),
    ]

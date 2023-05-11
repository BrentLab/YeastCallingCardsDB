# Generated by Django 4.2 on 2023-05-11 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('callingcards', '0008_hops_s3_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('uploadDate', models.DateField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lab', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('notes', models.CharField(default='none', max_length=100)),
                ('modifiedBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_modifiedBy', to=settings.AUTH_USER_MODEL)),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_uploader', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'lab',
            },
        ),
    ]

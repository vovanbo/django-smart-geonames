# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('iso_3166_1_a2', models.CharField(max_length=2, serialize=False, verbose_name='ISO 3166-1 alpha-2', primary_key=True)),
                ('iso_3166_1_a3', models.CharField(unique=True, max_length=3, verbose_name='ISO 3166-1 alpha-3')),
                ('iso_3166_1_numeric', models.CharField(unique=True, max_length=3, verbose_name='ISO 3166-1 numeric')),
                ('fips', models.CharField(max_length=2, verbose_name='FIPS', blank=True)),
                ('area', models.DecimalField(verbose_name='Area (km\xb2)', max_digits=15, decimal_places=5, blank=True)),
                ('population', models.BigIntegerField(verbose_name='Population', blank=True)),
                ('tld', models.CharField(max_length=2, verbose_name='Top-level domain', blank=True)),
                ('currency_code', models.CharField(db_index=True, max_length=3, verbose_name='Currency code', blank=True)),
                ('postal_code_format', models.CharField(max_length=255, verbose_name='Postal code format', blank=True)),
                ('postal_code_regex', models.CharField(max_length=255, verbose_name='Postal code regular expression', blank=True)),
                ('languages', models.CharField(max_length=255, verbose_name='List of languages spoken in a country', blank=True)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='GeoNameRecord',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.IntegerField(serialize=False, verbose_name='GeoName ID', primary_key=True)),
                ('name_ascii', models.CharField(max_length=255, verbose_name='Name in ASCII')),
                ('alt_names', models.TextField(max_length=10000, verbose_name='Alternate names')),
                ('feature_class', models.CharField(max_length=1, verbose_name='Feature class')),
                ('feature_code', models.CharField(max_length=10, verbose_name='Feature code', db_index=True)),
                ('admin1_code', models.CharField(max_length=20, verbose_name='Code for the first administrative division', blank=True)),
                ('admin2_code', models.CharField(max_length=80, verbose_name='Code for the second administrative division', blank=True)),
                ('admin3_code', models.CharField(max_length=20, verbose_name='Code for the third administrative division', blank=True)),
                ('admin4_code', models.CharField(max_length=20, verbose_name='Code for the fourth administrative division', blank=True)),
                ('population', models.BigIntegerField(verbose_name='Population', blank=True)),
                ('elevation', models.IntegerField(verbose_name='Elevation', blank=True)),
                ('dem', models.IntegerField(verbose_name='Digital elevation model', blank=True)),
                ('timezone', models.CharField(max_length=40, verbose_name='Timezone', blank=True)),
                ('modification_date', models.DateField(verbose_name='Modification date')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('country', models.ForeignKey(related_name='geo_names', verbose_name='Country', blank=True, to='smartgeonames.Country', null=True)),
            ],
            options={
                'verbose_name': 'GeoName',
                'verbose_name_plural': 'GeoNames',
            },
        ),
        migrations.CreateModel(
            name='GeoNameRecordTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='smartgeonames.GeoNameRecord', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'smartgeonames_geonamerecord_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'GeoName Translation',
            },
        ),
        migrations.CreateModel(
            name='PostalCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('code', models.CharField(max_length=20, verbose_name='Postal code', db_index=True)),
                ('place_name', models.CharField(max_length=180, verbose_name='Place name')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('accuracy', models.PositiveIntegerField()),
                ('admin1', models.OneToOneField(related_name='admin1_postal_code', null=True, blank=True, to='smartgeonames.GeoNameRecord', verbose_name='GeoName record for the first administrative division')),
                ('admin2', models.OneToOneField(related_name='admin2_postal_code', null=True, blank=True, to='smartgeonames.GeoNameRecord', verbose_name='GeoName record for the second administrative division')),
                ('admin3', models.OneToOneField(related_name='admin3_postal_code', null=True, blank=True, to='smartgeonames.GeoNameRecord', verbose_name='GeoName record for the third administrative division')),
                ('country', models.ForeignKey(related_name='postal_codes', verbose_name='Country', to='smartgeonames.Country')),
            ],
            options={
                'verbose_name': 'Postal code',
                'verbose_name_plural': 'Postal codes',
            },
        ),
        migrations.AddField(
            model_name='country',
            name='geo_name',
            field=models.OneToOneField(related_name='country_object', null=True, blank=True, to='smartgeonames.GeoNameRecord', verbose_name='GeoName record'),
        ),
        migrations.AddField(
            model_name='country',
            name='neighbours',
            field=models.ManyToManyField(related_name='_country_neighbours_+', verbose_name='Neighbours', to='smartgeonames.Country', blank=True),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
            ],
            options={
                'verbose_name': 'City',
                'proxy': True,
                'verbose_name_plural': 'Cities',
            },
            bases=('smartgeonames.geonamerecord',),
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
            ],
            options={
                'verbose_name': 'Continent',
                'proxy': True,
                'verbose_name_plural': 'Continents',
            },
            bases=('smartgeonames.geonamerecord',),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
            ],
            options={
                'verbose_name': 'Region',
                'proxy': True,
                'verbose_name_plural': 'Regions',
            },
            bases=('smartgeonames.geonamerecord',),
        ),
        migrations.AlterUniqueTogether(
            name='geonamerecordtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='country',
            name='capital',
            field=models.ForeignKey(related_name='capital_of', verbose_name='Capital', blank=True, to='smartgeonames.City', null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='continent',
            field=models.ForeignKey(related_name='countries', verbose_name='Continent', blank=True, to='smartgeonames.Continent', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='country',
            unique_together=set([('iso_3166_1_a2', 'iso_3166_1_a3', 'iso_3166_1_numeric')]),
        ),
    ]

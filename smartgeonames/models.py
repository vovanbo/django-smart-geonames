# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.contrib.gis.db.models import PointField
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from parler.models import TranslatableModel, TranslatedFields
from treebeard.mp_tree import MP_Node

from .managers import ContinentManager, CountryManager, RegionManager, \
    CityManager

CONTINENT_CHOICES = (
    ('AF', _('Africa')),
    ('AS', _('Asia')),
    ('EU', _('Europe')),
    ('NA', _('North America')),
    ('OC', _('Oceania')),
    ('SA', _('South America')),
    ('AN', _('Antarctica')),
)


class GeoNamesRecord(TimeStampedModel, TranslatableModel, MP_Node):
    geonameid = models.IntegerField(_('GeoNames ID'), primary_key=True)
    translations = TranslatedFields(
            name=models.CharField(_('Name'), max_length=255),
    )
    asciiname = models.CharField(_('Name in ASCII'), max_length=255)
    alternatenames = models.TextField(_('Alternate names'), max_length=10000,
                                      blank=True, null=True)
    feature_class = models.CharField(_('Feature class'), max_length=1)
    feature_code = models.CharField(_('Feature code'), max_length=10,
                                    db_index=True)
    country_info = models.ForeignKey('smartgeonames.CountryInfo',
                                     verbose_name=_('Country info'),
                                     related_name='geo_names',
                                     blank=True, null=True)
    admin1_code = models.CharField(
            _('Code for the 1st administrative division'), max_length=20,
            blank=True)
    admin2_code = models.CharField(
            _('Code for the 2nd administrative division'), max_length=80,
            blank=True)
    admin3_code = models.CharField(
            _('Code for the 3rd administrative division'), max_length=20,
            blank=True)
    admin4_code = models.CharField(
            _('Code for the 4th administrative division'), max_length=20,
            blank=True)
    population = models.BigIntegerField(_('Population'), blank=True)
    elevation = models.IntegerField(_('Elevation'), blank=True)
    dem = models.IntegerField(_('Digital elevation model'), blank=True)
    timezone = models.CharField(_('Timezone'), max_length=40, blank=True)
    modification_date = models.DateField(_('Modification date'))
    # latitude & longitude
    location = PointField()

    class Meta:
        verbose_name = _('GeoNames record')
        verbose_name_plural = _('GeoNames records')


class Continent(GeoNamesRecord):
    class Meta:
        proxy = True
        verbose_name = _('Continent')
        verbose_name_plural = _('Continents')

    objects = ContinentManager()


class Country(GeoNamesRecord):
    class Meta:
        proxy = True
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    objects = CountryManager()


class Region(GeoNamesRecord):
    class Meta:
        proxy = True
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')

    objects = RegionManager()


class City(GeoNamesRecord):
    class Meta:
        proxy = True
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    objects = CityManager()


class CountryInfo(TimeStampedModel, models.Model):
    iso_3166_1_a2 = models.CharField(_('ISO 3166-1 alpha-2'), max_length=2,
                                     primary_key=True)
    iso_3166_1_a3 = models.CharField(_('ISO 3166-1 alpha-3'), max_length=3,
                                     unique=True)
    iso_3166_1_numeric = models.CharField(_('ISO 3166-1 numeric'), max_length=3,
                                          unique=True)
    fips = models.CharField(_('FIPS'), max_length=2, blank=True)
    country = models.OneToOneField('smartgeonames.Country',
                                   verbose_name=_('GeoNames country record'),
                                   related_name='info',
                                   blank=True, null=True)
    capital = models.ForeignKey('smartgeonames.City',
                                verbose_name=_('Capital'),
                                related_name='capital_of',
                                blank=True, null=True)
    area = models.DecimalField(
            _('Area (km²)'),
            max_digits=15,
            decimal_places=5,
            blank=True)
    population = models.BigIntegerField(_('Population'), blank=True)
    continent = models.ForeignKey('smartgeonames.Continent',
                                  verbose_name=_('Continent'),
                                  related_name='countries',
                                  blank=True, null=True)
    tld = models.CharField(_('Top-level domain'), max_length=2, blank=True)
    currency_code = models.CharField(_('Currency code'), max_length=3,
                                     db_index=True, blank=True)
    postal_code_format = models.CharField(_('Postal code format'),
                                          max_length=255, blank=True)
    postal_code_regex = models.CharField(_('Postal code regular expression'),
                                         max_length=255, blank=True)
    languages = models.CharField(_('List of languages spoken in a country'),
                                 max_length=255, blank=True)
    neighbours = models.ManyToManyField('smartgeonames.Country',
                                        verbose_name=_('Neighbours'),
                                        symmetrical=True, blank=True)

    class Meta:
        unique_together = [
            'iso_3166_1_a2',
            'iso_3166_1_a3',
            'iso_3166_1_numeric'
        ]
        verbose_name = _('Country info')
        verbose_name_plural = _('Countries info')


class PostalCode(TimeStampedModel, models.Model):
    country = models.ForeignKey('smartgeonames.Country',
                                related_name='postal_codes',
                                verbose_name=_('Country'))
    code = models.CharField(_('Postal code'), max_length=20, db_index=True)
    place_name = models.CharField(_('Place name'), max_length=180)
    admin1 = models.OneToOneField(
            'smartgeonames.GeoNamesRecord',
            verbose_name=_(
                'GeoNames record for the 1st administrative division'),
            related_name='admin1_postal_code',
            blank=True, null=True)
    admin2 = models.OneToOneField(
            'smartgeonames.GeoNamesRecord',
            verbose_name=_(
                'GeoNames record for the 2nd administrative division'),
            related_name='admin2_postal_code',
            blank=True, null=True)
    admin3 = models.OneToOneField(
            'smartgeonames.GeoNamesRecord',
            verbose_name=_(
                'GeoNames record for the 3rd administrative division'),
            related_name='admin3_postal_code',
            blank=True, null=True)
    # latitude & longitude
    location = PointField()
    accuracy = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Postal code')
        verbose_name_plural = _('Postal codes')

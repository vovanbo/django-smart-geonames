# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db import models

from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from .managers import ContinentManager, CityManager, RegionManager

CONTINENT_CHOICES = (
    ('AF', _('Africa')),
    ('AS', _('Asia')),
    ('EU', _('Europe')),
    ('NA', _('North America')),
    ('OC', _('Oceania')),
    ('SA', _('South America')),
    ('AN', _('Antarctica')),
)


class GeoNameRecord(TranslatableModel):
    id = models.IntegerField(_('GeoName ID'), primary_key=True)
    translations = TranslatedFields(
        name = models.CharField(_('Name'), max_length=255),
    )
    name_ascii = models.CharField(_('Name in ASCII'), max_length=255)
    alt_names = models.TextField(_('Alternate names'), max_length=10000)
    feature_class = models.CharField(_('Feature class'), max_length=1)
    feature_code = models.CharField(_('Feature code'), max_length=10,
                                    db_index=True)
    country = models.ForeignKey('smartgeonames.Country',
                                verbose_name=_('Country'),
                                blank=True, null=True)
    admin1_code = models.CharField(
        _('Code for the first administrative division'), max_length=20,
        blank=True
    )
    admin2_code = models.CharField(
        _('Code for the second administrative division'), max_length=80,
        blank=True
    )
    admin3_code = models.CharField(
        _('Code for the third administrative division'), max_length=20,
        blank=True
    )
    admin4_code = models.CharField(
        _('Code for the fourth administrative division'), max_length=20,
        blank=True
    )
    population = models.BigIntegerField(_('Population'), blank=True)
    elevation = models.IntegerField(_('Elevation'), blank=True)
    dem = models.IntegerField(_('Digital elevation model'), blank=True)
    timezone = models.CharField(_('Timezone'), max_length=40, blank=True)
    modification_date = models.DateField(_('Modification date'))
    # latitude
    # longitude


class Continent(GeoNameRecord):
    class Meta:
        proxy = True

    objects = ContinentManager()


class Country(models.Model):
    iso_3166_1_a2 = models.CharField(_('ISO 3166-1 alpha-2'), max_length=2,
                                     primary_key=True)
    iso_3166_1_a3 = models.CharField(_('ISO 3166-1 alpha-3'), max_length=3,
                                     unique=True)
    iso_3166_1_numeric = models.CharField(_('ISO 3166-1 numeric'), max_length=3,
                                          unique=True)
    fips = models.CharField(_('FIPS'), max_length=2, blank=True)
    geoname = models.OneToOneField('smartgeonames.GeoNameRecord',
                                   verbose_name=_('GeoName record'),
                                   blank=True, null=True)
    capital = models.ForeignKey('smartgeonames.City',
                                verbose_name=_('Capital'),
                                blank=True, null=True)
    area = models.PositiveIntegerField(_('Area (km²)'), blank=True)
    population = models.BigIntegerField(_('Population'), blank=True)
    continent = models.ForeignKey('smartgeonames.Continent',
                                  verbose_name=_('Continent'),
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
    neighbours = models.ManyToManyField('self', verbose_name=_('Neighbours'),
                                        symmetrical=True, blank=True, null=True)

    class Meta:
        unique_together = [
            'iso_3166_1_a2',
            'iso_3166_1_a3',
            'iso_3166_1_numeric'
        ]


class Region(GeoNameRecord):
    class Meta:
        proxy = True

    objects = RegionManager()


class City(GeoNameRecord):
    class Meta:
        proxy = True

    objects = CityManager()


class PostalCode(models.Model):
    country = models.ForeignKey('smartgeonames.Country',
                                verbose_name=_('Country'))
    code = models.CharField(_('Postal code'), max_length=20, db_index=True)
    place_name = models.CharField(_('Place name'), max_length=180)
    admin1 = models.OneToOneField(
        'smartgeonames.GeoNameRecord',
        verbose_name=_('GeoName record for the first administrative division'),
        blank=True, null=True
    )
    admin2 = models.OneToOneField(
        'smartgeonames.GeoNameRecord',
        verbose_name=_('GeoName record for the second administrative division'),
        blank=True, null=True
    )
    admin3 = models.OneToOneField(
        'smartgeonames.GeoNameRecord',
        verbose_name=_('GeoName record for the third administrative division'),
        blank=True, null=True
    )
    admin4 = models.OneToOneField(
        'smartgeonames.GeoNameRecord',
        verbose_name=_('GeoName record for the fourth administrative division'),
        blank=True, null=True
    )
    # latitude
    # longitude
    # accuracy

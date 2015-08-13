# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os

import purl
from django.conf import settings

from .schemas import (CountryInfoSchema,
                      GeoNameSchema,
                      AlternateNameSchema,
                      PostalCodeSchema)

# Common
GEONAMES_URL = getattr(
    settings, 'SMART_GEONAMES_URL',
    'http://download.geonames.org'
)

DATA_DIR = getattr(
    settings, 'SMART_GEONAMES_DATA_DIR',
    os.path.normpath(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'data')
    )
)

# Countries
COUNTRIES_FILE_PATH = getattr(
    settings, 'SMART_GEONAMES_COUNTRIES_FILE_PATH',
    purl.URL(GEONAMES_URL).path('/export/dump/countryInfo.txt').as_string()
)
COUNTRIES_FILE_LOCAL_PATH = getattr(
    settings, 'SMART_GEONAMES_COUNTRIES_FILE_LOCAL_PATH',
    os.path.join(DATA_DIR, 'dump', 'countryInfo.txt')
)
COUNTRIES_SCHEMA = getattr(
    settings, 'SMART_GEONAMES_COUNTRIES_SCHEMA',
    CountryInfoSchema
)
COUNTRIES_FILTER = getattr(
    settings, 'SMART_GEONAMES_COUNTRIES_FILTER',
    {}
)

# GeoName objects
OBJECTS_FILE_PATH = getattr(
    settings, 'SMART_GEONAMES_OBJECTS_FILE_PATH',
    purl.URL(GEONAMES_URL).path('/export/dump/allCountries.zip').as_string()
)
OBJECTS_FILE_LOCAL_PATH = getattr(
    settings, 'SMART_GEONAMES_OBJECTS_FILE_LOCAL_PATH',
    os.path.join(DATA_DIR, 'dump', 'allCountries.zip')
)
OBJECTS_SCHEMA = getattr(
    settings, 'SMART_GEONAMES_OBJECTS_SCHEMA',
    GeoNameSchema
)
OBJECTS_CONTINENTS_FILTER = getattr(
    settings, 'SMART_GEONAMES_OBJECTS_CONTINENTS_FILTER',
    ('CONT',)
)
OBJECTS_COUNTRIES_FILTER = getattr(
    settings, 'SMART_GEONAMES_OBJECTS_COUNTRIES_FILTER',
    ('PCL',
     'PCLD',
     'PCLF',
     'PCLI',)
)
OBJECTS_REGIONS_FILTER = getattr(
    settings, 'SMART_GEONAMES_OBJECTS_REGIONS_FILTER',
    ('ADM1',)
)
OBJECTS_CITIES_FILTER = getattr(
    settings, 'SMART_GEONAMES_OBJECTS_CITIES_FILTER',
    ('PPL',
     'PPLA',
     'PPLA2',
     'PPLC',)
)
OBJECTS_FILTER = getattr(
    settings, 'SMART_GEONAMES_OBJECTS_FILTER',
    {
        'feature_code':
            OBJECTS_CONTINENTS_FILTER +
            OBJECTS_COUNTRIES_FILTER +
            OBJECTS_REGIONS_FILTER +
            OBJECTS_CITIES_FILTER,
        'country_code': ('RU',
                         'UA',),
    }
)

# Alternate Names (translations etc.)
TRANSLATIONS_FILE_PATH = getattr(
    settings, 'SMART_GEONAMES_TRANSLATIONS_FILE_PATH',
    purl.URL(GEONAMES_URL).path('/export/dump/alternateNames.zip').as_string()
)
TRANSLATIONS_FILE_LOCAL_PATH = getattr(
    settings, 'SMART_GEONAMES_TRANSLATIONS_FILE_LOCAL_PATH',
    os.path.join(DATA_DIR, 'dump', 'alternateNames.zip')
)
TRANSLATIONS_SCHEMA = getattr(
    settings, 'SMART_GEONAMES_TRANSLATIONS_SCHEMA',
    AlternateNameSchema
)
TRANSLATIONS_FILTER = getattr(
    settings, 'SMART_GEONAMES_TRANSLATIONS_FILTER',
    {
        'isolanguage': ('ru',
                        'ua',)
    }
)

# Postal codes
POSTAL_CODES_FILE_PATH = getattr(
    settings, 'SMART_GEONAMES_POSTAL_CODES_FILE_PATH',
    purl.URL(GEONAMES_URL).path('/export/zip/allCountries.zip').as_string()
)
POSTAL_CODES_FILE_LOCAL_PATH = getattr(
    settings, 'SMART_GEONAMES_POSTAL_CODES_FILE_LOCAL_PATH',
    os.path.join(DATA_DIR, 'zip', 'allCountries.zip')
)
POSTAL_CODES_SCHEMA = getattr(
    settings, 'SMART_GEONAMES_POSRAL_CODES_SCHEMA',
    PostalCodeSchema
)
POSTAL_CODES_FILTER = getattr(
    settings, 'SMART_GEONAMES_POSTAL_CODES_FILTER',
    {
        'country_code': ('RU',
                         'UA',)
    }
)

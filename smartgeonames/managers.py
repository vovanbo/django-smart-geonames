# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db import models

from .settings import (OBJECTS_CONTINENTS_FILTER,
                       OBJECTS_COUNTRIES_FILTER,
                       OBJECTS_CITIES_FILTER,
                       OBJECTS_REGIONS_FILTER)


class ContinentManager(models.Manager):
    def get_queryset(self):
        return super(ContinentManager, self).get_queryset().filter(
            featrue_code__in=OBJECTS_CONTINENTS_FILTER
        )


class CountryManager(models.Manager):
    def get_queryset(self):
        return super(CountryManager, self).get_queryset().filter(
            feature_code__in=OBJECTS_COUNTRIES_FILTER
        )


class CityManager(models.Manager):
    def get_queryset(self):
        return super(CityManager, self).get_queryset().filter(
            feature_code__in=OBJECTS_CITIES_FILTER
        )


class RegionManager(models.Manager):
    def get_queryset(self):
        return super(RegionManager, self).get_queryset().filter(
            feature_code__in=OBJECTS_REGIONS_FILTER
        )
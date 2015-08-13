# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartgeonames', '0002_auto_20150812_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='area',
            field=models.DecimalField(verbose_name='Area (km\xb2)', max_digits=15, decimal_places=5, blank=True),
        ),
    ]

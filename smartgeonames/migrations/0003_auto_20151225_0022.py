# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgeonames', '0002_auto_20151225_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geonamesrecord',
            name='elevation',
            field=models.IntegerField(null=True, verbose_name='Elevation', blank=True),
        ),
    ]

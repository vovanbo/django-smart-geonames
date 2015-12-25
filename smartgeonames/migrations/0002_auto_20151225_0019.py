# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgeonames', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geonamesrecord',
            name='admin2_code',
            field=models.CharField(max_length=80, null=True, verbose_name='Code for the 2nd administrative division', blank=True),
        ),
        migrations.AlterField(
            model_name='geonamesrecord',
            name='admin3_code',
            field=models.CharField(max_length=20, null=True, verbose_name='Code for the 3rd administrative division', blank=True),
        ),
        migrations.AlterField(
            model_name='geonamesrecord',
            name='admin4_code',
            field=models.CharField(max_length=20, null=True, verbose_name='Code for the 4th administrative division', blank=True),
        ),
    ]

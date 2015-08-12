# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('smartgeonames', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 21, 47, 51, 822320, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 21, 48, 0, 590355, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='geonamerecord',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 21, 48, 7, 582117, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='geonamerecord',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 21, 48, 12, 93905, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postalcode',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 21, 48, 17, 469829, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postalcode',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 21, 48, 25, 661612, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]

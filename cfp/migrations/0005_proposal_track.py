# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-17 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0004_proposal_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='track',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
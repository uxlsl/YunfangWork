# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0003_auto_20170322_0745'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuxiliaryNotFound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agentname', models.CharField(blank=True, db_column='AgentName', max_length=255, null=True)),
                ('agenttelephone', models.CharField(blank=True, db_column='AgentTelephone', max_length=30, null=True)),
                ('agency', models.CharField(blank=True, db_column='Agency', max_length=255, null=True)),
                ('agentstores', models.CharField(blank=True, db_column='AgentStores', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='备份时间')),
            ],
        ),
    ]
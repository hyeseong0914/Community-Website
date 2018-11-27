# Generated by Django 2.0.6 on 2018-06-29 05:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=120)),
                ('hit', models.IntegerField(default=0)),
                ('content', models.TextField()),
                ('post_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('file_name', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('file_size', models.IntegerField(default=0)),
                ('down', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('board_id', models.IntegerField()),
                ('author', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('post_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
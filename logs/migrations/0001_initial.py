# Generated by Django 3.2 on 2021-04-19 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('method', models.CharField(max_length=50)),
                ('uri', models.CharField(max_length=2000)),
                ('status_code', models.IntegerField(null=True)),
                ('size', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

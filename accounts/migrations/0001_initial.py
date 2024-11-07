# Generated by Django 5.0.7 on 2024-11-06 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=40)),
                ('secondName', models.CharField(blank=True, max_length=40)),
                ('lastName', models.CharField(max_length=40)),
                ('mail', models.EmailField(max_length=254, unique=True)),
                ('birth', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
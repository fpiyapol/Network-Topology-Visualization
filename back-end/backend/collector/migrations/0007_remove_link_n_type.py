# Generated by Django 2.2.1 on 2019-05-08 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0006_link_n_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='n_type',
        ),
    ]

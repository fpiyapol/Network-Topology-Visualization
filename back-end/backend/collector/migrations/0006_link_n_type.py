# Generated by Django 2.2.1 on 2019-05-08 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0005_device_ip_addr'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='n_type',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]

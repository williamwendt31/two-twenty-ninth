# Generated by Django 2.1.1 on 2018-12-22 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_admin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address2',
        ),
    ]
# Generated by Django 3.2.10 on 2023-02-02 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outpass_locator', '0010_auto_20230202_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outpass_locator_staff_details',
            name='outpass_type_id',
        ),
    ]

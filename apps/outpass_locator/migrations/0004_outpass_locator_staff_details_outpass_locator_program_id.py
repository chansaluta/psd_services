# Generated by Django 3.2.10 on 2023-01-12 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outpass_locator', '0003_outpass_locator_program'),
    ]

    operations = [
        migrations.AddField(
            model_name='outpass_locator_staff_details',
            name='outpass_locator_program_id',
            field=models.IntegerField(null=True),
        ),
    ]

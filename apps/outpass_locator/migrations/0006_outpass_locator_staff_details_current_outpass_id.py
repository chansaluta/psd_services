# Generated by Django 3.2.10 on 2023-01-12 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outpass_locator', '0005_outpass_locator_staff_details_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='outpass_locator_staff_details',
            name='current_outpass_id',
            field=models.IntegerField(null=True),
        ),
    ]
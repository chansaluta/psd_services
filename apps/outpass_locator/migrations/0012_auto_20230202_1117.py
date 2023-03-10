# Generated by Django 3.2.10 on 2023-02-02 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outpass_locator', '0011_remove_outpass_locator_staff_details_outpass_type_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='official_outpass_locator_logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(max_length=16)),
                ('user_id', models.IntegerField()),
                ('outpass_locator_staff_details_id', models.IntegerField()),
                ('inclusive_dates', models.TextField()),
                ('time_check_out', models.CharField(max_length=16)),
                ('time_check_in', models.CharField(max_length=16)),
                ('time_span_outpass', models.CharField(max_length=16)),
                ('month', models.CharField(max_length=12, null=True)),
                ('remarks', models.TextField(null=True)),
                ('place_visited', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'official_outpass_locator_logs',
            },
        ),
        migrations.RemoveField(
            model_name='outpass_locator_logs',
            name='outpass_type_id',
        ),
        migrations.RemoveField(
            model_name='outpass_locator_logs',
            name='remarks',
        ),
    ]

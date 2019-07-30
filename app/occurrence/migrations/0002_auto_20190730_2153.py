# Generated by Django 2.2.3 on 2019-07-30 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('occurrence', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='category',
            field=models.CharField(choices=[('CONSTRUCTION', 'planned road work'), ('SPECIAL_EVENT', 'special events (fair, sport event, etc.)'), ('INCIDENT', 'accidents and other unexpected events'), ('WHEATHER_CONDITION', 'weather condition affecting the road'), ('ROAD_CONDITION', 'status of the road that might affect travellers     (potholes, bad pavement, etc)')], max_length=20),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='state',
            field=models.CharField(choices=[('NOT_VALIDATED', 'not validated'), ('VALIDATED', 'validated'), ('RESOLVED', 'resolved')], max_length=20),
        ),
    ]
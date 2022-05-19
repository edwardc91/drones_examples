# Generated by Django 3.2 on 2022-05-19 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('start_datetime', models.DateTimeField(null=True, verbose_name='Start datetime')),
                ('arrive_datetime', models.DateTimeField(null=True, verbose_name='Arrived')),
                ('was_delivered', models.BooleanField(default=False, verbose_name='Was delivered?')),
                ('drone_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.drone', verbose_name='Drone')),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(default=1, verbose_name='Quantity')),
                ('flight_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.flight', verbose_name='Flight')),
                ('medication_rel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.medication', verbose_name='Medication')),
            ],
            options={
                'unique_together': {('flight_rel', 'medication_rel')},
            },
        ),
    ]

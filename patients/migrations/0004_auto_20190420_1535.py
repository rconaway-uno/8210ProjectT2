# Generated by Django 2.0.5 on 2019-04-20 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20190414_1202'),
        ('patients', '0003_auto_20190420_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='arrival_condition',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='patient',
            name='arrival_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='mode_of_arrival',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='patient',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.Organization'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='room_number',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='patient',
            name='tag_color_condition',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='patient',
            name='triage_tag_num',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]

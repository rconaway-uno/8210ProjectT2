# Generated by Django 2.0.5 on 2019-04-22 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0005_auto_20190422_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disposition',
            name='transfer_to_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Organization'),
        ),
    ]

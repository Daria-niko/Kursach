# Generated by Django 4.2.17 on 2024-12-12 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedCare', '0005_alter_medicalcard__insurance_policy_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractionlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MedCare.user'),
        ),
    ]

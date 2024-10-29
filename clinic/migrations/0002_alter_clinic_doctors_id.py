# Generated by Django 4.2.14 on 2024-10-29 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_doctor_user'),
        ('clinic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='doctors_id',
            field=models.ManyToManyField(related_name='doctor', to='doctor.doctor'),
        ),
    ]

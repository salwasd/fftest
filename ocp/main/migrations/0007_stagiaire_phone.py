# Generated by Django 4.2.3 on 2023-08-03 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_convocation_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='stagiaire',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-18 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='position',
            field=models.CharField(blank=True, default='-', max_length=200, null=True),
        ),
    ]

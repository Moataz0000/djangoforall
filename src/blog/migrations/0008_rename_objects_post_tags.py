# Generated by Django 5.1.2 on 2024-10-19 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_objects'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='objects',
            new_name='tags',
        ),
    ]

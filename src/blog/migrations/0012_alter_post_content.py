# Generated by Django 5.1.2 on 2024-10-19 14:13

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text'),
        ),
    ]

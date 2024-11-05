# Generated by Django 5.1.2 on 2024-10-23 00:25

import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('main_image', models.ImageField(blank=True, default='no_picture.jpg', upload_to='projects')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Content')),
                ('github_url', models.URLField()),
                ('deploy_url', models.URLField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='no_picture.jpg', upload_to='projects')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='portfolio.project')),
            ],
        ),
    ]
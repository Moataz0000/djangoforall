# Generated by Django 5.1.2 on 2024-10-14 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='no_picture.jpg', upload_to='posts'),
        ),
    ]

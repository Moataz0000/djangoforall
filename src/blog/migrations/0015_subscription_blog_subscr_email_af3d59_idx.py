# Generated by Django 5.1.2 on 2024-10-25 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_subscription'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['email'], name='blog_subscr_email_af3d59_idx'),
        ),
    ]
# Generated by Django 3.1.6 on 2024-11-20 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_nickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_email_verified',
        ),
    ]

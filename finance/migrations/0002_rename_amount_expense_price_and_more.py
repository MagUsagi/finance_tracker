# Generated by Django 5.0.1 on 2024-08-12 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='amount',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='income',
            old_name='amount',
            new_name='price',
        ),
    ]

# Generated by Django 5.0.1 on 2024-08-12 15:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('amount', models.BigIntegerField(verbose_name='Amount')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finance.assetcategory', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('amount', models.IntegerField(verbose_name='Amount')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finance.expensecategory', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('amount', models.IntegerField(verbose_name='Amount')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finance.incomecategory', verbose_name='Category')),
            ],
        ),
    ]
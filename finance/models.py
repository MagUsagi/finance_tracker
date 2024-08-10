from django.db import models

# Create your models here.

# Payment Category
class PaymentCategory(models.Model):
    name = models.CharField('Category', max_length=32)

    def __str__(self):
        return self.name
    
# Payment
class Payment(models.Model):
    date = models.DateField('Date')
    amount = models.IntegerField('Amount')
    category = models.ForeignKey(PaymentCategory, on_delete=models.PROTECT, verbose_name="Category")
    description = models.TextField('Description', null=True, blank=True)

# Income Category
class IncomeCategory(models.Model):
    name = models.CharField('Category', max_length=32)

    def __str__(self):
        return self.name
    
# Income
class Income(models.Model):
    date = models.DateField('Date')
    amount = models.IntegerField('Amount')
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT, verbose_name="Category")
    description = models.TextField('Description', null=True, blank=True)

# Asset Category
class AssetCategory(models.Model):
    name = models.CharField('Category', max_length=32)

    def __str__(self):
        return self.name
    
# Asset
class Asset(models.Model):
    date = models.DateField('Date')
    amount = models.BigIntegerField('Amount')
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT, verbose_name="Category")
    description = models.TextField('Description', null=True, blank=True)
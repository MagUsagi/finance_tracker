from django.contrib import admin
from .models import Expense, Income, ExpenseCategory, IncomeCategory
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ExpenseResource(resources.ModelResource):
    class Meta:
        model = Expense


class ExpenseAdmin(ImportExportModelAdmin):
    search_fields = ('description',)
    list_display = ['date', 'category', 'price', 'description']
    list_filter = ('category',)
    ordering = ('-date',)

    resource_class = ExpenseResource


class ExpenceCategoryResource(resources.ModelResource):
    class Meta:
        model = ExpenseCategory


class ExpenseCategoryAdmin(ImportExportModelAdmin):
    resource_class = ExpenceCategoryResource


class IncomeResouce(resources.ModelResource):
    class Meta:
        model = Income


class IncomeAdmin(ImportExportModelAdmin):
    search_fields = ('description',)
    list_display = ['date', 'category', 'price', 'description']
    list_filter = ('category',)
    ordering = ('-date',)

    resource_class = IncomeResouce


class IncomeCategoryResource(resources.ModelResource):
    class Meta:
        model = IncomeCategory


class IncomeCategoryAdmin(ImportExportModelAdmin):
    resource_class = IncomeCategoryResource


admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
admin.site.register(IncomeCategory, IncomeCategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Income, IncomeAdmin)
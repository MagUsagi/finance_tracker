from django import forms
from .models import PaymentCategory, Payment, IncomeCategory, Income, AssetCategory, Asset
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError

# Create and return year options
def year_choices():
    start_year = settings.FINANCE_START_YEAR
    end_year = datetime.now().year
    years = [(year, year) for year in reversed(range(start_year,end_year + 1))]
    years.insert(0, (0, ''))

    return tuple(years)

# Create and return month options
def month_choices():
    months = [(month, str(month).rjust(2,'0')) for month in range(1, 13)]
    months.insert(0, (0, ''))

    return tuple(months)

year_choice_field = forms.ChoiceField(
    label='Filter by year',
    required=False,
    choices=year_choices(),
    widget=forms.Select(attrs={'class': 'form-select form-select-sm', 'value': ''})
)
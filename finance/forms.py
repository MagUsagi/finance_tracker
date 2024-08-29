from django import forms
from .models import ExpenseCategory, Expense, IncomeCategory, Income, AssetCategory, Assets
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from .widgets import CustomRadioSelect

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

month_choice_field = forms.ChoiceField(
    label='filter by month',
    required=False,
    choices=month_choices(),
    widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
)

create_form_widgets= {
    'date': forms.DateInput(attrs={'autocomplete': 'off',
                                   'placeholder': 'date',
                                   'class': 'form-control',
                                   "type":"date"}),
    'category': forms.Select(attrs={'class': 'form-select'}),
    'price': forms.TextInput(attrs={'autocomplete': 'off',
                                     'placeholder': 'amount',
                                     'class': 'form-control'}),
    'description': forms.Textarea(attrs={'autocomplete': 'off',
                                         'placeholder': 'description',
                                         'class': 'form-control',
                                         'rows': '2'}),
}

# Expense search form
class ExpenseSearchForm(forms.Form):

    year = year_choice_field

    month = month_choice_field

    greater_than = forms.IntegerField(
        label='Greater Than',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                      'autocomplete': 'off',
                                      'placeholder': 'anmount Greater Than'})
    )

    less_than = forms.IntegerField(
        label='Less Than',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                          'autocomplete': 'off',
                                          'placeholder': 'amount Less Than'})
    )

    key_word = forms.CharField(
        label='Search',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                      'autocomplete': 'off',
                                      'placeholder': 'Keyword'})
    )

    search_category = forms.ModelChoiceField(
        label='Filter by Category',
        required=False,
        queryset=ExpenseCategory.objects.order_by('name'),
        widget=CustomRadioSelect
    )

# Income search form
class IncomeSearchForm(forms.Form):
    year = year_choice_field
    month = month_choice_field

# Assets search form
class AssetsSearchForm(forms.Form):
    year = year_choice_field
    month = month_choice_field

    search_category = forms.ModelChoiceField(
        label='Filter by Category',
        required=False,
        queryset=AssetCategory.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )

# Expense Registration Form
class ExpenseNewForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = create_form_widgets


# Income Regisration Form
class IncomeNewForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'
        widgets = create_form_widgets

# Filtering form for transition graphs
class TransitionGraphSearchForm(forms.Form):
    SHOW_CHOICES = (
        ('ALL', 'All'),
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    )

    Expense_category = forms.ModelChoiceField(
        label='Filter by Expense Category',
        required=False,
        queryset=ExpenseCategory.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
    )

    income_category = forms.ModelChoiceField(
        label='Filter by Income Category',
        required=False,
        queryset=IncomeCategory.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
    )

    graph_visible = forms.ChoiceField(required=False,
                                      label='Visible Graphs',
                                      choices=SHOW_CHOICES,
                                      widget=forms.Select(attrs={'class': 'form-select form_select-sm'}),
                                      )
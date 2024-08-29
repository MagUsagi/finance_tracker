from django.shortcuts import render
from django.views import generic
from .models import Expense, ExpenseCategory, Income, IncomeCategory
from .forms import ExpenseSearchForm, IncomeSearchForm, ExpenseNewForm, IncomeNewForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from .plugin_plotly import GraphGenerator

# Create your views here.

# Dashboard (index page)
class Dashboard(generic.TemplateView):
    template_name = 'finance/dashboard.html'


# Monthly Dashboard
class MonthDashboard(generic.TemplateView):
    template_name = 'finance/month_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        context['year_month'] = f'{year}.{month}'

        # previous month and next month in context
        if month == 1:
            prev_year = year - 1
            prev_month = 12
        else:
            prev_year = year
            prev_month = month - 1

        if month == 12:
            next_year = year + 1
            next_month = 1
        else:
            next_year = year
            next_month = month + 1

        context['prev_year'] = prev_year
        context['prev_month'] = prev_month
        context['next_year'] = next_year
        context['next_month'] = next_month

        ''' Glaph '''
        # make the Expense model df
        queryset = Expense.objects.filter(date__year=year)
        queryset = queryset.filter(date__month=month)
        # If the query set is empty, return context
        if not queryset:
            return context
        
        df = read_frame(queryset,
                        fieldnames=['date', 'price', 'category'])
        
        # Instantiate a graph creation class
        gen = GraphGenerator()

        # Create elements for pie chart
        # Pivot totals of amounts per category
        df_pie = pd.pivot_table(df, index='category', values='price', aggfunc="sum")
        # Plotly needs to be in list format.
        pie_labels = list(df_pie.index.values)
        pie_values = [val[0] for val in df_pie.values]
        plot_pie = gen.month_pie(labels=pie_labels, values=pie_values)
        context['plot_pie'] = plot_pie
 
        # For displaying categories and prices in table
        # Create a dictionary of {category:price, category: price...}
        context['table_set'] = df_pie.to_dict()['price']

        # Calculate and pass on the total figure
        context['total_expense'] = df['price'].sum()

        # Create elements for the daily bar chart
        df_bar = pd.pivot_table(df, index='date', values='price', aggfunc="sum")
        dates = list(df_bar.index.values)
        heights = [val[0] for val in df_bar.values]
        plot_bar = gen.month_daily_bar(x_list=dates, y_list=heights)
        context['plot_bar'] = plot_bar

        return context

# Transition
class TransitionView(generic.TemplateView):
    # Monthly income and expense transition
    template_name = 'finance/transition.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense_queryset = Expense.objects.all()
        income_queryset = Income.objects.all()

        expense_df = read_frame(expense_queryset,
                               fieldnames=['date', 'price'])
        # Convert date columns to datetime and convert to Y-m notation
        expense_df['date'] = pd.to_datetime(expense_df['date'])
        expense_df['month'] = expense_df['date'].dt.strftime('%Y-%m')
        # Monthly PIVOT tally
        expense_df = pd.pivot_table(expense_df, index='month', values='price', aggfunc="sum")
        # x-axis
        months_expense = list(expense_df.index.values)
        # y-axis
        expenses = [y[0] for y in expense_df.values]

        # Income is also created on the x- and y-axes in the same way
        income_df = read_frame(income_queryset,
                               fieldnames=['date', 'price'])
        income_df['date'] = pd.to_datetime(income_df['date'])
        income_df['month'] = income_df['date'].dt.strftime('%Y-%m')
        # Monthly PIVOT tally
        income_df = pd.pivot_table(income_df, index='month', values='price', aggfunc="sum")
        # x-axis
        months_income = list(income_df.index.values)
        # y-axis
        incomes = [y[0] for y in income_df.values]

        # graph generation
        gen = GraphGenerator()
        context['transition_plot'] = gen.transition_plot(x_list_expense=months_expense,
                                                        y_list_expense=expenses,
                                                        x_list_income=months_income,
                                                        y_list_income=incomes)
        
        return context


# Expence List
class ExpenseList(generic.ListView):
    template_name = 'finance/expense_list.html'
    model = Expense
    ordering = '-date'
    paginate_by = 10  # show 10 datas on 1 page

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = ExpenseSearchForm(self.request.GET or None)

        if form.is_valid():

             # Excluded because a string of 0 is entered when nothing is selected
            year = form.cleaned_data.get('year')
            if year and year != '0':
                queryset = queryset.filter(date__year=year)
            
            # Excluded because a string of 0 is entered when nothing is selected
            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

            # greater than
            greater_than = form.cleaned_data.get('greater_than')
            if greater_than:
                queryset = queryset.filter(price__gte=greater_than)
            
            # less than
            less_than = form.cleaned_data.get('less_than')
            if less_than:
                queryset = queryset.filter(price__lte=less_than)
            
            # Keywords
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                # Separate by blank, filter in order, AND search
                if key_word:
                    for word in key_word.split():
                        queryset = queryset.filter(description__icontains=word)
                
            # Category
            category = form.cleaned_data.get('search_category')
            if category:
                #queryset = queryset.filter(category=category)
                queryset = queryset.filter(category__isnull=True)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass search form
        context['search_form'] = self.form

        return context
    
# Expense Registration 
class ExpenseNew(generic.CreateView):
    template_name = 'finance/register.html'
    model = Expense
    form_class = ExpenseNewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'New Expense'
        return context
    
    def get_success_url(self):
        return reverse_lazy('finance:expense_list')
    
    # Display a success message when validated
    def form_valid(self, form):
        self.object = expense = form.save()
        messages.info(self.request,
                      f'Expenses registered.\n'
                      f'Date: {expense.date}\n'
                      f'Category: {expense.category}\n'
                      f'Price: {expense.price} chf')
        return redirect(self.get_success_url())
    
# Expencse Update (Edit)
class ExpenseUpdate(generic.UpdateView):
    template_name = 'finance/register.html'
    model = Expense
    form_class = ExpenseNewForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Update Expense'
        return context
    
    def get_success_url(self):
        return reverse_lazy('finance:expense_list')
    
    def form_valid(self, form):
        self.object = expense = form.save()
        messages.info(self.request,
                      f'Expense updated\n'
                      f'Date: {expense.date}\n'
                      f'Category: {expense.category}\n'
                      f'Price: {expense.price} chf')
        return redirect(self.get_success_url())
    
# Expense Delete
class ExpenseDelete(generic.DeleteView):
    template_name = 'finance/delete.html'
    model = Expense

    def get_success_url(self):
        return reverse_lazy('finance:expense_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Delete Expense'
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = expense = self.get_object()
        expense.delete()
        messages.info(self.request,
                      f'Expense deleted\n'
                      f'Date: {expense.date}\n'
                      f'Category: {expense.category}\n'
                      f'Price: {expense.price} chf')
        return redirect(self.get_success_url())    

# Income List
class IncomeList(generic.ListView):
    template_name = 'finance/income_list.html'
    model = Income
    ordering = '-date'
    paginate_by = 10  # show 10 datas on 1 page

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = IncomeSearchForm(self.request.GET or None)

        if form.is_valid():

             # Excluded because a string of 0 is entered when nothing is selected
            year = form.cleaned_data.get('year')
            if year and year != '0':
                queryset = queryset.filter(date__year=year)
            
            # Excluded because a string of 0 is entered when nothing is selected
            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass search form
        context['search_form'] = self.form

        return context
    
# Income Registration
class IncomeNew(generic.CreateView):
    template_name = 'finance/register.html'
    model = Income
    form_class = IncomeNewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'New Income'
        return context
    
    def get_success_url(self):
        return reverse_lazy('finance:income_list')
    
    # Display a success message when validated
    def form_valid(self, form):
        self.object = income = form.save()
        messages.info(self.request,
                      f'Income registered.\n'
                      f'Date: {income.date}\n'
                      f'Category: {income.category}\n'
                      f'Price: {income.price} chf')
        return redirect(self.get_success_url())
    
# Income Update (Edit)
class IncomeUpdate(generic. UpdateView):
    template_name = 'finance/register.html'
    model = Income
    form_class = IncomeNewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Update Income'
        return context
    
    def get_success_url(self):
        return reverse_lazy('finance:income_list')
    
    def form_valid(self, form):
        self.object = income = form.save()
        messages.info(self.request,
                      f'Income Updated\n'
                      f'Date: {income.date}\n'
                      f'Category: {income.category}\n'
                      f'Price: {income.price} chf')
        return redirect(self.get_success_url())
    
# Income Delete
class IncomeDelete(generic.DeleteView):
    template_name = 'finance/delete.html'
    model = Income

    def get_success_url(self):
        return reverse_lazy('finance:income_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Delete Income'
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = income = self.get_object()
        income.delete()
        messages.info(self.request,
                      f'Income deleted\n'
                      f'Date: {income.date}\n'
                      f'Category: {income.category}\n'
                      f'Price: {income.price} chf')
        return redirect(self.get_success_url())   

# Assets
def Assets(request):
    return render(request, 'finance/assets.html')

# Category 
def Category(request):
    return render(request, 'finance/category.html')

# Payee
def Payee(request):
    return render(request, 'finance/payee.html')
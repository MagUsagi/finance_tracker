from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('expense_list/', views.ExpenseList.as_view(), name='expense_list'),
    path('income_list/', views.IncomeList.as_view(), name='income_list'),
    path('expense_new/', views.ExpenseNew.as_view(), name='expense_new'),
    path('income_new/', views.IncomeNew.as_view(), name='income_new'),
    path('expense_update/<int:pk>/', views.ExpenseUpdate.as_view(), name='expense_update'),
    path('income_update/<int:pk>/', views.IncomeUpdate.as_view(), name='income_update'),
    path('expense_delete/<int:pk>/', views.ExpenseDelete.as_view(), name='expense_delete'),
    path('income_delete/<int:pk>/', views.IncomeDelete.as_view(), name='income_delete'),
    path('month_dashboard<int:year>/<int:month>', views.MonthDashboard.as_view(), name='month_dashboard'),
    path('transition/', views.TransitionView.as_view(), name='transition'),
    path('assets/', views.Assets, name='assets'),
    path('category/', views.Category, name='category'),
    path('payee/', views.Payee, name='payee'),
]
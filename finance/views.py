from django.shortcuts import render

# Create your views here.

# Dashboard (index page)
def dashboard(request):
    return render(request, 'finance/dashboard.html')
from django.shortcuts import render

# Create your views here.
def stock_home(request):
    return render(request, 'stock_home.html')

def stock_watchlist(request):
    return render(request, 'watchlist.html')

def stock_details(request):
    return render(request, 'details.html')
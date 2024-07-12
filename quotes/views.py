# Copyright (c) 2024-2025 Lee Brooks All Rights Reserved
 
from contextlib import redirect_stderr
import re
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
    import requests 
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']
        # pk_5a38a369954d45da9d37a459d9088484
        api_request = requests.get("https://api.iex.cloud/v1/data/core/iex_tops/" + ticker + "?token=pk_5a38a369954d45da9d37a459d9088484")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error"
        return render(request, 'home.html', {'api': api})
    
    else:
        return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})


    
def about(request):
    import pprint

    cat = {'name': 'Zophie', 'age': 7, 'color': 'gray'}
    allCats = []
    allCats.append({'name': 'Zophie', 'age': 7, 'color': 'gray'})
    allCats.append({'name': 'Pooka', 'age': 5, 'color': 'black'})
    allCats.append({'name': 'Fat-tail', 'age': 4, 'color': 'orange'})
    allCats.append({'name': '???', 'age': -1, 'color': 'tan'}) 


    allCatsEx = '''cat = {'name': 'Zophie', 'age': 7, 'color': 'gray'} 
    allCats = [] 

    allCats.append({'name': 'Zophie', 'age': 7, 'color': 'gray'}) 

    allCats.append({'name': 'Pooka', 'age': 5, 'color': 'black'}) 

    allCats.append({'name': 'Fat-tail', 'age': 4, 'color': 'orange'}) 

    allCats.append({'name': '???', 'age': -1, 'color': 'tan'})
    
    allCats
    '''

    theBoard = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ','mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ','low-L': ' ', 'low-M': ' ', 'low-R': ' '}
    
    pprint.pprint(theBoard)

    howToPPrint = '''
    theBoard = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ','mid-L': ' ', 'mid-M': 'X', 'mid-R': ' ','low-L': ' ', 'low-M': ' ', 'low-R': ' '}
    
    printBoard = pprint.pprint(theBoard)

    '''

    return render(request, 'about.html', {'allCats': allCats, 'allCatsEx': allCatsEx, 'theBoard': theBoard, 'howToPPrint': howToPPrint})

def add_stock(request):
    import requests 
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added!"))
            return redirect('add_stock')

    else:
        ticker = Stock.objects.all()
        output = []

        for ticker_item in ticker:
            api_request = requests.get("https://api.iex.cloud/v1/data/core/iex_tops/" + str(ticker_item) + "?token=pk_5a38a369954d45da9d37a459d9088484")

            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."
        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, "Stock Has Been Deleted!")
    return redirect(delete_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})



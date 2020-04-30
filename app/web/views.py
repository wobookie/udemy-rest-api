from django.shortcuts import render

context = {
    'title': 'Hello World!',
}

def home(request):
    return render(request, 'web/home.html')

def index(request):
    return render(request, 'base.html')
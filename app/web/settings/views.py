from django.shortcuts import render

context = {
    'title': 'Hello World!',
}

def tokens(request):
    return render(request, 'web/settings/tokens.html')
from django.shortcuts import render


def index(request):
    # template = 'web/index.html'
    template = 'web/login.html'

    return render(request, template_name=template)

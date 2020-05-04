from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_auth_login
from django.contrib.auth.decorators import login_required, permission_required
from django.views.defaults import page_not_found
import logging

logger = logging.getLogger('__name__')

@login_required
def home(request):
    template = 'web/home.html'

    return render(request, template_name=template)

def index(request):
    # template = 'web/index.html'
    template = 'web/login.html'

    return render(request, template_name=template)

def login(request):
    template = 'web/login.html'

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_auth_login(request, user)
            logger.debug('Login for user <%s> successful !', str(user))
            return redirect('web:home')
        else:
            logger.debug('Login attempt with username <%s> failed!', username)
    return render(request, template_name=template)

def handler_404(request, exception):
    template = 'web/errors/404.html'

    return page_not_found(request, exception, template_name=template)
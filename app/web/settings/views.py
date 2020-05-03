from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def tokens(request):
    template = 'web/settings/tokens.html'

    context = {
        'title': 'Hello World!',
    }


    return render(request, template_name=template, context=context)
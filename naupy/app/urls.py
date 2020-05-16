"""naupy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, path, include
from .views import index


urlpatterns = [
    path('', index, name='index'),
    re_path(r'^web/', include('web.urls', namespace='web')),
    re_path(r'^api/', include('api.urls', namespace='api')),
    path('admin/', admin.site.urls),
]

# custom handle of 404 server error
handler404 = 'web.views.handler_404'

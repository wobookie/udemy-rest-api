from django.conf.urls import url

from . import views

urlpatterns = [
    url('', views.healthcheck, name='healthcheck'),
]

app_name = 'api_healthcheck'

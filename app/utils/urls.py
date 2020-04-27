from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

from . import views

urlpatterns = [
    url('health-check/', views.health_check, name='health-check'),
]

app_name = 'utils'

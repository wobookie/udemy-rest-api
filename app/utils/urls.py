from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^health-check$', views.health_check, name='health-check'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
app_name = 'utils'

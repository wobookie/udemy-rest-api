from django.conf.urls import url

from api.healthcheck import views

urlpatterns = [
    url('health-check/', views.health_check, name='health-check'),
]

app_name = 'api'

from django.urls import path

from . import views as views
from rest_framework_simplejwt import views as jwt_views


app_name = 'users'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
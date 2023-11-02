from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('local-login/', views.local_login, name='local_login')
]
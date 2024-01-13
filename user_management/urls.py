from django.urls import path
from .views import get_and_send_code, account_login

urlpatterns = [
    path('login_action', get_and_send_code, name='phone_login'),
    path('login', account_login, name='account_login'),

]
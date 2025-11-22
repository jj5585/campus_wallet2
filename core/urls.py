from django.urls import path
from .views import (
    dashboard,
    topup_view,
    pay_view,
    LoginView,
    logout_view,
    register_view,   # 👈 import the new view
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('register/', register_view, name='register'),  # 👈 public signup route
    path('topup/', topup_view, name='topup'),
    path('pay/', pay_view, name='pay'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]

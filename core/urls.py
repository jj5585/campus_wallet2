from django.urls import path
from .views import dashboard, topup_view, pay_view, LoginView, logout_view

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('topup/', topup_view, name='topup'),
    path('pay/', pay_view, name='pay'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]

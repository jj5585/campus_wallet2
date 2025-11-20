from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('maria/', admin.site.urls),
    path('', include('core.urls')),
]

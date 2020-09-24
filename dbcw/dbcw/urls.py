from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('portfolios.urls')),
    path('admin/', admin.site.urls),
]

from django.urls import path

from . import views


urlpatterns = [
    path('', views.root, name='root'),
    path('home/', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('join/', views.join, name='join'),
]

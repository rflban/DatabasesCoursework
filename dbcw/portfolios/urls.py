from django.urls import path

from . import views


urlpatterns = [
    path('', views.root, name='root'),
    path('home/', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('search/<str:searching>', views.search, name='search'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('join/', views.join, name='join'),
    path('profile/', views.profile, name='profile'),
    path('create/', views.create, name='create'),
    path('user/<str:username>', views.user, name='user'),
    path('portfolio/<int:portfolio_id>', views.portfolio, name='portfolio'),
    path('post/<int:post_id>', views.post, name='post'),
]

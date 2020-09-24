from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User

from . import forms


def minimal_context(request):
    return {
            'is_authenticated': request.user.is_authenticated
    }


def root(request):
    return redirect('home')

def index(request):
    context = minimal_context(request)
    return render(request, 'portfolios/index.html', context)


def about(request):
    context = minimal_context(request)
    return render(request, 'portfolios/about.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        auth_user_form = forms.AuthUserForm(request.POST)

        if auth_user_form.is_valid:
            username = auth_user_form.data['username']
            password = auth_user_form.data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('home')
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        auth_user_form = forms.AuthUserForm()

    context = minimal_context(request)
    context['auth_user_form'] = auth_user_form

    return render(request, 'portfolios/login.html', context)


def join(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user_form = forms.UserForm(request.POST)
        profile_form = forms.ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            profile = profile_form.save(commit=False)

            user = User.objects.create_user(
                user_form.data['username'],
                user_form.data['email'],
                user_form.data['password'],
            )

            user.first_name = user_form.data['first_name']
            user.last_name = user_form.data['last_name']
            user.save()

            profile.user_id = user
            profile.save()

            return redirect('login')

    else:
        user_form = forms.UserForm()
        profile_form = forms.ProfileForm()

    context = minimal_context(request)
    context['user_form'] = user_form
    context['profile_form'] = profile_form

    return render(request, 'portfolios/join.html', context)

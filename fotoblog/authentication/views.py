from django.contrib.auth import login, authenticate, logout # import des fonctions login et authenticate
from django.shortcuts import redirect, render
from . import forms
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            message = 'Identifiants invalides.'
    return render(
        request, 'login.html', context={'form': form, 'message': message})

def logout_user(request):
    
    logout(request)
    return redirect('login')

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(
        request, 'signup.html', context={'form': form})
    

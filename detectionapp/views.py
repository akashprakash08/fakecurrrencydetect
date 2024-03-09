from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, LoginForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'detectionapp/index.html')
 
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my-login')
        else:
            # If form is not valid, print form.errors to debug
            print(form.errors)
        
    context = {'registerform' :form}
    return render(request, 'detectionapp/register.html', context=context)

def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
    
    context = {'loginform': form}
    return render(request, 'detectionapp/my-login.html', context=context)

@login_required
def dashboard(request):
    
    username = request.user.username
    email = request.user.email
    context = {'username': username, 'email': email}
    return render(request, 'detectionapp/dashboard.html', context=context)

def user_logout(request):
    logout(request)
    return redirect(reverse('homepage'))
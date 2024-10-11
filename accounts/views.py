from django.shortcuts import render, redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

def register(request):
    if request.method == "POST":
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # Password authenticator
        if password == password2:
            # Username  and email checker
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already in use")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email,
                first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, "Registration successful")
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username,password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')
    
def logout(request):
    return redirect('accounts/login.html')
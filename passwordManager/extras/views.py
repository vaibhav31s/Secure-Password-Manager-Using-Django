
from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import random
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from django.core.mail import send_mail

def home(request):
    if request.method == 'POST':
        if "signup-form" in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('password2')
            #if password is mismatched
            if password != confirmPassword:
                msg = "Please enter Right password in both fields"
                messages.error(request,msg)
                return HttpResponseRedirect(request.path)
            #if username exists
            elif User.objects.filter(username=username).exists():
                msg = f"{username} already exists!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            elif User.objects.filter(email=email).exists():
                msg = f"{email} already exists !"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                User.objects.create_user(username,email,password)
                new_user = authenticate(request,username=username,password=confirmPassword)
                if new_user is not None:
                    login(request, new_user)
                    msg = f"{username}. Thanks for Joinning in to US. keep the security to US leave all worries"
                    messages.success(request,msg)
                    return HttpResponseRedirect(request.path)
        if "logout" in request.POST:
            msg =f"{request.user} Your logout successfully."
            logout(request)
            messages.success(request,msg)
            return HttpResponseRedirect(request.path)

        if "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            new_login = authenticate(request, username=username, password=password)
            if new_login is None:
                msg = f"Login failed! Make sure you're using the right account."
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                code = str(random.randint(100000, 999999))
                send_mail(
                    'Django Password Manager: confirm email',
                    f'Your verification code is {code}',
                    settings.EMAIL_HOST_USER,
                    [new_login.email],
                    fail_silently=False,
                )
                return render(request, "home.html", {
                    "code":code, 
                    "user":new_login,
                })
               


    return render(request,"home.html",{})
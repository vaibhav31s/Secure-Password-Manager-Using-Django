
import types
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
import os
from twilio.rest import Client
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import random
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from django.core.mail import send_mail
from decouple import config
from .models import Passwords,newUser
fernet = Fernet(settings.KEY)
br = Browser()
br.set_handle_robots(False)


def home(request):
    if request.method == "POST":
        if "signup-form" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            mobile = request.POST.get('phone')
            #if password are not identical
            if password != password2:
                msg = "Please make sure you're using the same password!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            #if username exists
            elif User.objects.filter(username=username).exists():
                msg = f"{username} already exists!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            #if email exists
            elif User.objects.filter(email=email).exists():
                msg = f"{email} already exists!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                
                User.objects.create_user(username, email, password)
                new_user = authenticate(request, username=username, password=password2)
                
                # newextendeduser = newUser(mobile=mobile)
                
                if new_user is not None:
                    login(request, new_user)
                    msg = f"{username}. Thanks for subscribing."
                    messages.success(request, msg)
                    newextendeduser =newUser.objects.create(user =new_user,mobile=mobile)
                    newextendeduser.save()
                    return HttpResponseRedirect(request.path)
        elif "logout" in request.POST:
            msg = f"{request.user}. You logged out."
            logout(request)
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)

        elif 'login-model' in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            new_login = authenticate(request, username=username, password=password)
            if new_login is None:
                msg = f"Login failed! Make sure you're using the right account."
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            elif new_login is None:
                code = str(random.randint(100000, 999999))
                global global_code
                global_code = code
                send_mail(
                    "Django Password Manager: confirm email",
                    f"Your verification code is {code}.",
                    settings.EMAIL_HOST_USER,
                    [new_login.email],
                    fail_silently=False,
                )
                return render(request, "home.html", {
                    "code":code, 
                    "user":new_login,
                })
            else:
                new_user = authenticate(request, username=username, password=password)
                if new_user is not None:
                    login(request, new_user)
                    msg = f"{username}. Welocme."
                    messages.success(request, msg)
                    return HttpResponseRedirect(request.path)

        elif "confirm" in request.POST:
                input_code= request.POST.get("code")
                user = request.POST.get('user')
                if input_code != global_code:
                    msg= f"{input_code} is wrong"
                    messages.success(request,msg)
                    return HttpResponseRedirect(request.path)
                else:
                    login(request,User.objects.get(username=user))
                    msg= f"{request.user} Welcome Again My friend."
                    messages.success(request,msg)
                    return HttpResponseRedirect(request.path)


        elif "add-password" in request.POST:
            url = request.POST.get("url")
            email = request.POST.get("email")
            password = request.POST.get("password")

            #encryting password and email with fernet 
            encrypted_email = fernet.encrypt(email.encode())
            encrypted_password = fernet.encrypt(password.encode())

            #get the title of the website we are storing data of
            br.open(url)
            title = br.title()

            #get the logo of the website we are storing data of (Scrarping all the images on the website and taking only the first one image So we can set it to Its icon)
            icon = favicon.get(url)[0].url

            new_password =Passwords.objects.create(
                user = request.user,
                name= title,
                logo = icon,
                email = encrypted_email.decode(),
                password = encrypted_password.decode(),
                 
            )
            msg = f"{title} Added Successfully"
            messages.success(request,msg)
            return HttpResponseRedirect(request.path)

        elif "add-password" in request.POST:
                url = request.POST.get("url")
                email = request.POST.get("email")
                password = request.POST.get("password")
                #ecrypt data
                encrypted_email = fernet.encrypt(email.encode())
                encrypted_password = fernet.encrypt(password.encode())
                #get title of the website
                try:
                    br.open(url)
                    title = br.title()
                except:
                    title = url
                #get the logo's URL
                try:
                    icon = favicon.get(url)[0].url
                except:
                    icon = "https://cdn-icons-png.flaticon.com/128/1006/1006771.png"
                #Save data in database
                new_password = Passwords.objects.create(
                    user=request.user,
                    name=title,
                    logo=icon,
                    email=encrypted_email.decode(),
                    password=encrypted_password.decode(),
                )
                msg = f"{title} added successfully."
                messages.success(request, msg)
                return HttpResponseRedirect(request.path)

        elif "send" in request.POST:
            ids = request.POST.get('password-id')

            print(ids)
            userId =Passwords.objects.filter(id=ids).values('user_id')
            print(userId[0]['user_id'])
            getEmail = User.objects.filter(id=userId[0]['user_id']).values('email')
            mobileno = newUser.objects.filter(user_id=userId[0]['user_id']).values('mobile')
            print(mobileno[0]['mobile'])
            print(getEmail[0]['email'])
            mob =mobileno[0]['mobile']

            # tai = User.objects.values()
            # print(tai)
            vaibhav = Passwords.objects.filter(id=ids).values('password','email')
            my_str = (vaibhav[0]['password'])
            password = str.encode(my_str)
            my_str1 =str(mob)
            my_str2 = (vaibhav[0]['email'])
            email = str.encode(my_str2)
          
            # email = fernet.decrypt(vaibhav.get('email').encode()).decode()
            ps= fernet.decrypt(password).decode()
            print(ps)
            em = fernet.decrypt(email).decode()
            print(em)
            # send_mail(
            #     "Password for : ",
            #     f"Your UserName is {em} .\n Password is {ps}",
            #     settings.EMAIL_HOST_USER,
            #     [getEmail[0]['email']],
            #     fail_silently=False,
            # )
            
            account_sid = config('account_sid')
            auth_token = config('auth_token')
            client = Client(account_sid, auth_token)

            message = client.messages \
                            .create(
                                body= f"Your UserName is {em} .\n Password is {ps}",
                                from_='+17069404471',
                                to='+91'+my_str1
                            )

            print(message.sid)
            msg =f"Message is Delivered Successful ly"
            messages.success(request, msg)

        # elif "delete" in request.POST:
            
        #     toshow = request.POST.get("password-id")
        #     data = Passwords.objects.get(id=toshow)
        #     # passwords = Passwords.objects.get(id=toshow)
            
        #     user = User.objects.all().filter(id=toshow)
        #     print(user)
    

        #     # send_mail(
        #     #         "Password for is{username}: ",
        #     #         f"Your UserName is {passwords.get('User') }.\n Password is {password}",
        #     #         settings.EMAIL_HOST_USER,
        #     #         ['gawadvaibhavv@gmail.com'],
        #     #         fail_silently=False,
        #     #     )
        #     return render(request, "home.html", {
        #             "passwords":passwords,
        #         })

    context = {}
    if request.user.is_authenticated:
        passwords = Passwords.objects.all().filter(user=request.user)
        for password in passwords:
            password.email = fernet.decrypt(password.email.encode()).decode()
            password.password = fernet.decrypt(password.password.encode()).decode()
        context = {
            "passwords":passwords,
        }   
    return render(request,"index.html",context)

def logins(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        user = authenticate(request, username=username, password=password)
        login(request, user)
        msg = f"{username}. Welocme."
        messages.success(request, msg)
        return redirect('/')      
    return render(request,"login.html",{})

def index(request):
    context = {}
    if request.user.is_authenticated:
        passwords = Passwords.objects.all().filter(user=request.user)
        for password in passwords:
            password.email = fernet.decrypt(password.email.encode()).decode()
            password.password = fernet.decrypt(password.password.encode()).decode()
        context = {
            "passwords":passwords,
        }   
    return render(request,"index.html",context)

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']
        phone = request.POST['phone']
        print(username)
        print(email)
        print(pass1)
        print(pass2)
        print(phone)
        if User.objects.filter(username=username):
            messages.error(request,"Username is allready exist!")
            return redirect('/')
        if User.objects.filter(email=email):
            messages.error(request,"email is allready exist!")
            return redirect('/')
        if pass1!= pass2:
            messages.error(request,"Password didnt match")
        

        myuser = User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request,"Your account has been succesfully created!")

        return redirect('login')
        
    return render(request,"sign-up.html",{})

def add(request):
    if request.method == "POST":
        url = request.POST["url"]
        email = request.POST["email"]
        password = request.POST["password"]
        print(url)
        print(email)
        print(password)
        
        #encryting password and email with fernet 
        encrypted_email = fernet.encrypt(email.encode())
        encrypted_password = fernet.encrypt(password.encode())

        #get the title of the website we are storing data of
        br.open(url)
        title = br.title()

        #get the logo of the website we are storing data of (Scrarping all the images on the website and taking only the first one image So we can set it to Its icon)
        icon = favicon.get(url)[0].url

        new_password =Passwords.objects.create(
            user = request.user,
            name= title,
            logo = icon,
            email = encrypted_email.decode(),
            password = encrypted_password.decode(),
                
        )
        msg = f"{title} Added Successfully"
        messages.success(request,msg)
        return redirect('/')
    
    return render(request,"password.html",{})

def signout(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect('/')
# def home(request):
#     if request.method == 'POST':
#         if "signup-form" in request.POST:
#             username = request.POST.get('username')
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             confirmPassword = request.POST.get('password2')
#             #if password is mismatched
#             if password != confirmPassword:
#                 msg = "Please enter Right password in both fields"
#                 messages.error(request,msg)
#                 return HttpResponseRedirect(request.path)
#             #if username exists
#             elif User.objects.filter(username=username).exists():
#                 msg = f"{username} already exists!"
#                 messages.error(request, msg)
#                 return HttpResponseRedirect(request.path)
#             elif User.objects.filter(email=email).exists():
#                 msg = f"{email} already exists !"
#                 messages.error(request, msg)
#                 return HttpResponseRedirect(request.path)
#             else:
#                 User.objects.create_user(username,email,password)
#                 new_user = authenticate(request,username=username,password=confirmPassword)
#                 if new_user is not None:
#                     login(request, new_user)
#                     msg = f"{username}. Thanks for Joinning in to US. keep the security to US leave all worries"
#                     messages.success(request,msg)
#                     return HttpResponseRedirect(request.path)
#         if "logout" in request.POST:
#             msg =f"{request.user} Your logout successfully."
#             logout(request)
#             messages.success(request,msg)
#             return HttpResponseRedirect(request.path)

#         if "login-modal" in request.POST:
#             username = request.POST.get("username")
#             password = request.POST.get("password")
#             new_login = authenticate(request, username=username, password=password)
#             if new_login is None:
#                 msg = f"Login failed! Make sure you're using the right account."
#                 messages.error(request, msg)
#                 return HttpResponseRedirect(request.path)
#             if new_login is not None:
#                 code = str(random.randint(100000, 999999))
#                 send_mail( 'Django Password Manager: confirm email','Your verification code is {code}','gawadvaibhav31@gmail.com', ['gawadvaibhavv@gmail.com'],fail_silently=False,)

               
               


#     return render(request,"home.html",{})
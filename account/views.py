from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Profile

def sign_up (request: HttpRequest):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        if password != repeat_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'signUp.html')
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "A user with that username already exists.", "alert-danger")
            return render(request, "signUp.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with that email already exists.", "alert-danger")
            return render(request, "signUp.html") 
        
    if request.method == "POST":
        try:
            new_user = User.objects.create_user(username = request.POST["username"], password=request.POST["password"], email=request.POST["email"])
            new_user.save()
            messages.success(request, "You have been Registered Successfully", "alert-success")
            #send confirmation email
            content_html = render_to_string("mail/welcoming.html",{"userName":new_user}) #set email
            send_to = new_user.email
            email_message = EmailMessage("welcoming", content_html, settings.EMAIL_HOST_USER, [send_to])
            email_message.content_subtype = "html"
            #email_message.connection = email_message.get_connection(True)
            email_message.send()
            return redirect("account:log_in")
        except IntegrityError:
            messages.error(request, "An error occurred during registration.", "alert-danger")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}", "alert-danger")
    return render(request, "signUp.html")



def log_in(request: HttpRequest):
        
    if request.method == "POST":
   #checking user credentials
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user:
            #login the user
            login(request, user)
            messages.success(request, "You are Logged in successfully", "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Please try again. You credentials are wrong", "alert-danger")
    return render(request, 'logIn.html')


def log_out(request:HttpRequest):
    logout(request)
    messages.success(request, "You are logged out successfully", "alert-warning")

    return redirect(request.GET.get("next", "/"))

@login_required(login_url="account:log_in")
def profile_view(request:HttpRequest, user_name):
    try:
        user = User.objects.get(username=user_name)
        profile = Profile.objects.filter(user=user).first()
        
        if not profile:
            # Redirect to create_profile_view if profile doesn't exist
            return redirect('account:create_profile_view', user_name=user_name)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return render(request, "404.html")
    return render(request, "profile.html", {'profile': profile})

@login_required(login_url="account:log_in")
def create_profile_view(request:HttpRequest, user_name):
    user = get_object_or_404(User, username=user_name)

    if request.method == "POST":
        try:
            new_profile = Profile(
                user=user,  # Associate the profile with the user
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                age=request.POST["age"],
                hight=request.POST["hight"],
                wight=request.POST["wight"],
                phone=request.POST["phone"]
            )
            if 'avatar' in request.FILES:
                new_profile.avatar = request.FILES["avatar"]
            new_profile.save()
            messages.success(request, "Profile Created Successfully")
            return redirect('account:profile_view', user_name=user_name)
        except IntegrityError:
            messages.error(request, "An error occurred during Creating profile.", "alert-danger")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}", "alert-danger")
    return render(request,"addProfile.html", {'user': user})
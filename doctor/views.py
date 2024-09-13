from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from doctor.models import Doctor



@login_required(login_url="account:log_in")
def all_doctors_view(request: HttpRequest):
    doctor = Doctor.objects.all()

    return render(request, "allDoctors.html", {"doctors":doctor})

@login_required(login_url="account:log_in")
def add_doctors_view(request:HttpRequest):
    if request.method == "POST":

        name = request.POST["name"]
        email = request.POST["email"]
        # Check if user already exists
        if Doctor.objects.filter(name=name).exists():
            messages.error(request, "A user with that username already exists.", "alert-danger")
            return render(request, "addDoctors.html")
        
        if Doctor.objects.filter(email=email).exists():
            messages.error(request, "A user with that email already exists.", "alert-danger")
        
    if request.method == "POST":
        try:
            new_doctor = Doctor.objects.create(name = request.POST["name"], specialization=request.POST["specialization"], about=request.POST["about"],email=request.POST["email"],phone=request.POST["phone"],image=request.FILES["image"])
            new_doctor.save()
            messages.success(request, "Doctor has been Added Successfully", "alert-success")
        except IntegrityError:
            messages.error(request, "An error occurred during Creating Doctor.", "alert-danger")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}", "alert-danger")


    return render(request, "addDoctors.html")
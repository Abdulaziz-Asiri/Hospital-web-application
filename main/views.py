from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from clinic.models import Clinic
from doctor.models import Doctor
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from account.models import Profile
from appointment.models import Appointment
from datetime import datetime

def home_view(request:HttpRequest):
        clinic = Clinic.objects.prefetch_related('doctors_id').all()
        doctor = Doctor.objects.all()

        return render(request, "index.html",{"clinics":clinic, "doctors":doctor})

def details_clinics(request: HttpRequest, clinic_id):
    clinic = Clinic.objects.get(id=clinic_id)

    return render(request, "clinic_details.html", {"clinic":clinic})

def make_appointment(request: HttpRequest, clinic_id, profile_id):  
    clinic = Clinic.objects.get(id=clinic_id)
    doctor = Doctor.objects.all()
    user = User.objects.get(id=profile_id)
    profile = Profile.objects.get(user=user)
    context ={
         "clinic": clinic,
        "profile": profile,
        "doctor": doctor,
    }
    if not request.user.is_authenticated:
        messages.error(request,"Only registered users can access")
        return redirect("account:log_in")
    if request.method == "POST":
        try:
            doctor = Doctor.objects.get(id=request.POST['doctor'])
            date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
            time_slot = datetime.strptime(request.POST['time_slot'], '%H:%M').time()

            new_appointment = Appointment(
                user=profile,
                doctor=doctor,
                clinic=clinic,
                date=date,
                time_slot=time_slot,
            )
            new_appointment.save()
            content_html = render_to_string("appointment/templates/mail/confirmation.html",{"appointment":new_appointment}) 
            send_to = new_appointment.user.user.email 
            email_message = EmailMessage("Appointment Confirmation", content_html, settings.EMAIL_HOST_USER, [send_to])
            email_message.content_subtype = "html"
            email_message.send()
            messages.success(request, "Appointment has been Added Successfully")
            return redirect("appointment:all_appointment_view") 
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

    return render(request, "makeAppointment.html",context)

@login_required(login_url="account:log_in")
def dashboard_view(request:HttpRequest):

    return render(request, "dashboard.html")
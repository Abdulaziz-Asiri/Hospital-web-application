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
from patientSummary.models import PatientSummary
from appointment.models import Appointment
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home_view(request:HttpRequest):
        clinic = Clinic.objects.prefetch_related('doctors_id').all()
        doctor = Doctor.objects.all()

        return render(request, "index.html",{"clinics":clinic, "doctors":doctor})

def details_clinics(request: HttpRequest, clinic_id):
    clinic = Clinic.objects.get(id=clinic_id)
    return render(request, "clinic_details.html", {"clinic":clinic , })

@login_required(login_url="account:log_in")
def make_appointment(request:HttpRequest, clinic_id):  
    clinic = Clinic.objects.get(id=clinic_id)
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    doctor_ids = clinic.doctors_id.values_list('id', flat=True)

    context ={
        "clinic": clinic,
        "profile": profile,
    }
    if not request.user.is_authenticated:
                messages.error(request,"Only registered users can access")
                return redirect("account:log_in")
    
    if request.method == "POST":
        try:
            date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
            time_slot = datetime.strptime(request.POST['time_slot'], '%H:%M').time()
            
            user_appointment_exists = Appointment.objects.filter(
                user=profile, date=date
            ).exists()

            if user_appointment_exists:
                messages.error(request, "You already have an appointment on this day.")
                return redirect("main:make_appointment", clinic_id)
            else:
                new_appointment = Appointment(
                    user=profile,
                    clinic=clinic,
                    date=date,
                    time_slot=time_slot
                )
                new_appointment.save()

            # content_html = render_to_string("appointment/templates/mail/confirmation.html",{"appointment":new_appointment}) 
            # send_to = new_appointment.user.user.email 
            # email_message = EmailMessage("Appointment Confirmation", content_html, settings.EMAIL_HOST_USER, [send_to])
            # email_message.content_subtype = "html"
            # email_message.send()
            # messages.success(request, "Appointment has been Added Successfully")

            return redirect("appointment:my_appointment_view", user) 
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

    return render(request, "makeAppointment.html",context)

@login_required(login_url="account:log_in")
def dashboard_view(request:HttpRequest):
    appointments = Appointment.objects.all()
    appointmentCount = Appointment.objects.all()
    patitenReport = PatientSummary.objects.all()
    profiles = Profile.objects.all()
    users = Profile.objects.filter(user__is_staff=False, user__is_superuser=False)
    doctors = Doctor.objects.all()
    patientSummary = PatientSummary.objects.all()

    paginator = Paginator(appointments, 6)  # Show n items per page
    paginator2 = Paginator(profiles, 6)  # Show n items per page
    paginator3 = Paginator(patientSummary, 6)  # Show n items per page
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page_number)
        page_obj1 = paginator2.get_page(page_number)
        page_obj3 = paginator3.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page_obj = paginator.get_page(1)
        page_obj1 = paginator2.get_page(1)
        page_obj3 = paginator3.get_page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        page_obj = paginator.get_page(paginator.num_pages)
        page_obj1 = paginator2.get_page(paginator.num_pages)
        page_obj3 = paginator3.get_page(paginator.num_pages)


    context={
        "appointments":page_obj,
        "appointmentCount":appointmentCount,
        "patitenReport":patitenReport,
        "users":users,
        "doctors":doctors,
        "profile": page_obj1,
        "patientSummary": page_obj3
    }

    return render(request, "dashboard.html", context)

@login_required(login_url="account:log_in")
def doctor_dashboard_view(request:HttpRequest):

    return render(request, "doctorDash.html")


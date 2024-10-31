from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import authenticate
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from clinic.models import Clinic
from doctor.models import Doctor
from appointment.models import Appointment
from account.models import Profile
from patientSummary.models import PatientSummary
from django.contrib.auth.models import User
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q





@login_required(login_url="account:log_in")
def all_appointment_view(request: HttpRequest):
    if not request.user.is_staff:
        messages.error(request,"Only registered users can access")
        return redirect("account:log_in")
    else:
        appointment = Appointment.objects.all()

    return render(request, "allAppointment.html", {"appointments":appointment})

@login_required(login_url="account:log_in")
def all_doctor_appointment_view(request: HttpRequest):
    if not request.user.is_staff:
        messages.error(request,"Only registered users can access")
        return redirect("account:log_in")
    else:
        doctorProfile = get_object_or_404(Doctor, user=request.user)
        search_query = request.GET.get('search', '')
        appointment = Appointment.objects.filter(clinic__doctors_id=doctorProfile)

    if search_query:
        appointment = appointment.filter(
            Q(user__first_name__icontains=search_query) | Q(user__last_name__icontains=search_query) |  
            Q(date__icontains=search_query)  
        )
    paginator = Paginator(appointment, 6)  # Show n items per page

    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        page_obj = paginator.get_page(paginator.num_pages)


    return render(request, "doctorAppointment.html", {"appointments":page_obj, "search_query": search_query})


@login_required(login_url="account:log_in")
def my_appointment_view(request: HttpRequest, user_username):
    user = get_object_or_404(User, username=user_username)
    profile = get_object_or_404(Profile, user=user)
    appointments = Appointment.objects.filter(user=profile).prefetch_related('summaries')

    paginator = Paginator(appointments, 6)  # Show n items per page
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        "appointments": page_obj,
    }
    return render(request, "myAppointment.html", context)

@login_required(login_url="account:log_in")
def add_appointment_view(request: HttpRequest):
    doctors = Doctor.objects.all()
    clinics = Clinic.objects.all()
    users = Profile.objects.all()
    if not request.user.is_staff:
        messages.error(request,"Only registered users can access")
        return redirect("account:log_in")
    if request.method == "POST":
        try:
            user = Profile.objects.get(id=request.POST['user'])
            clinic = Clinic.objects.get(id=request.POST['clinic'])
            date = datetime.strptime(request.POST['date'], '%Y-%m-%d' ).date()
            time_slot = datetime.strptime(request.POST['time_slot'], '%H:%M').time()

            new_appointment = Appointment(
                user=user,
                clinic=clinic,
                date=date,
                time_slot=time_slot,
            )
            new_appointment.save()
            content_html = render_to_string("mail/confirmation.html",{"appointment":new_appointment}) 
            send_to = new_appointment.user.user.email 
            email_message = EmailMessage("Appointment Confirmation", content_html, settings.EMAIL_HOST_USER, [send_to])
            email_message.content_subtype = "html"
            email_message.send()
            
            messages.success(request, "Appointment has been Added Successfully")
            return redirect("appointment:all_appointment_view") 
        
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    
    context = {
        'doctors': doctors,
        'clinics': clinics,
        'users': users,
    }
    return render(request, "addAppointment.html", context)

@login_required(login_url="account:log_in")
def delete_appointment_view(request:HttpRequest, appointment_id):
    if not request.user.is_staff:
        messages.error(request,"Only registered users can delete")
        return redirect("account:log_in")
    try:
        appointment = Appointment.objects.get(id=appointment_id) # implement feedback messages
        appointment.delete()
        messages.success(request, "Appointment has been Deleted successfully", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete Appointment", "alert-danger")

    return redirect("appointment:all_appointment_view")

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointment.models import Appointment
from patientSummary.models import PatientSummary
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from doctor.models import Doctor
from django.db.models import Q

@login_required(login_url="account:log_in")
def display_patient_summary(request:HttpRequest, summary_id):
    summary = get_object_or_404(PatientSummary,id=summary_id)

    return render(request, "patientSummery.html", {"summary":summary})

@login_required(login_url="account:log_in")
def add_patient_summary(request: HttpRequest, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        try:
            new_summary = PatientSummary(
                appointment=appointment,
                diagnosis=request.POST['diagnosis'],
                prescription_name=request.POST['prescription_name']
            )
            new_summary.save()
            messages.success(request, "Patient summary added successfully.")
            if request.user.is_superuser:
                return redirect("patientSummary:all_patient_summary")
            else:
                return redirect("appointment:all_doctor_appointment_view")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    context = {
        'appointment': appointment,
    }
    return render(request, "add_patient_summary.html", context)

@login_required(login_url="account:log_in")
def all_patient_summary(request:HttpRequest):
    if not request.user.is_staff:
        messages.error(request,"Only registered users can access")
        return redirect("account:log_in")
    else:
        patientSummary = PatientSummary.objects.all()

        paginator = Paginator(patientSummary, 6)  # Show n items per page
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page.
            page_obj = paginator.get_page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            page_obj = paginator.get_page(paginator.num_pages)

    return render(request,"allPatientRecords.html",{"patientSummaries":page_obj})

@login_required(login_url="account:log_in")
def all_doctor_patient_summary(request:HttpRequest):
    if not request.user.is_staff:
        messages.error(request,"Only registered users can access")
        return redirect("account:log_in")
    else:
        doctorProfile = get_object_or_404(Doctor, user=request.user)
        search_query = request.GET.get('search', '')
        patientSummary = PatientSummary.objects.filter(appointment__clinic__doctors_id=doctorProfile)

    if search_query:
        patientSummary = patientSummary.filter(
            Q(appointment__user__first_name__icontains=search_query) | Q(appointment__user__last_name__icontains=search_query) 
        )

    paginator = Paginator(patientSummary, 6)  # Show n items per page
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request,"allDoctorPatient.html",{"patientSummaries":page_obj})

@login_required(login_url="account:log_in")
def delete_patient_summary(request:HttpRequest, record_id):
    if not request.user.is_staff:
        messages.error(request,"Only registered users can delete")
        return redirect("account:log_in")
    try:
        patientSummary = PatientSummary.objects.get(id=record_id) # implement feedback messages
        patientSummary.delete()
        messages.success(request, "Patient Record has been Deleted successfully", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete Patient Record", "alert-danger")

    return redirect("patientSummary:all_patient_summary")
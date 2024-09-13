from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from clinic.models import Clinic
from doctor.models import Doctor



@login_required(login_url="account:log_in")
def all_clinics_view(request: HttpRequest):
    clinic = Clinic.objects.prefetch_related('doctors_id').all()

    return render(request, "allClinic.html", {"clinics":clinic})
@login_required(login_url="account:log_in")
def details_clinics_view(request: HttpRequest, clinic_id):
    # clini_details = Clinic.objects.get(id=clinic_id)
    clinic = Clinic.objects.get(id=clinic_id)

    return render(request, "clinicDetails.html", {"clinic":clinic})

@login_required(login_url="account:log_in")
def add_clinics_view(request:HttpRequest):
    doctors = Doctor.objects.all()
    working_hours_choices = Clinic.WorkingHours.choices
    if request.method == "POST":
        name = request.POST["name"]
        if Clinic.objects.filter(name=name).exists():
            messages.error(request, "A Clinic with this name already exists.", "alert-danger")
        else:
            try:
                new_clinic = Clinic(
                    name=request.POST['name'],
                    description=request.POST['description'],
                    working_hours=request.POST['working_hours'],
                    feature_image=request.FILES['feature_image']
                )
                new_clinic.save()
                
                # Add selected doctors to the clinic
                doctor_ids = request.POST.getlist('doctors')
                new_clinic.doctors_id.set(doctor_ids)
                messages.success(request, "Clinic has been Added Successfully", "alert-success")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}", "alert-danger")
    context = {
    'doctors': doctors,
    'working_hours_choices': working_hours_choices,
    }
    return render(request, "addClinic.html", context)

# def add_products_view(request: HttpRequest):
    if not request.user.is_authenticated:
        messages.error(request,"Only registered users can access")
        return redirect("account:sign_in")
    products = Product.objects.all()
    category = Category.objects.all()
    allSuppliers = Supplier.objects.all() 
    if request.method == "POST":
        category_id = request.POST['category']
        category_instance = Category.objects.get(id=category_id)
        new_product = Product(name=request.POST['name'],
                                description=request.POST['description'],
                                price=request.POST['price'],
                                category= category_instance,
                                image= request.FILES['image'])
        new_product.save()
        supplier_ids = request.POST.getlist('suppliers')
        suppliers = Supplier.objects.filter(id__in=supplier_ids)
        new_product.suppliers.add(*suppliers)

    return render(request, "addProducts.html",  {"products": products,"categories":category,"suppliers": allSuppliers})
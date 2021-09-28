from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from datetime import date
from .models import Employee
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from . import views
from django.contrib.auth.decorators import login_required
import calendar
from django.db.models import Q 

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required 
def index(request):
    Customer = apps.get_model('customers.Customer')
    all_customers = Customer.objects.filter()
    logged_in_user = request.user

    if request.method == "POST":
        today = date.today()
        cust_id_post = request.POST.get('cust_id')
        customer_edit = Customer.objects.get(id=cust_id_post)
        customer_edit.date_of_last_pickup = today
        customer_edit.balance += 20
        customer_edit.save()

        return HttpResponseRedirect(reverse('employees:index'))
    else:
        try:
            today = date.today()
            day = calendar.day_name[today.weekday()]
            logged_in_employee = Employee.objects.get(user=logged_in_user)
            matched_customers = Customer.objects.filter(Q(zip_code = logged_in_employee.zipcode) & Q(one_time_pickup = today) | Q(weekly_pickup = day))
        
            context = {
                'logged_in_employee': logged_in_employee,
                'today': today,
                'Customer': all_customers,
                'Customers': matched_customers,
                'day': day
            }
            return render(request, 'employees/index.html', context)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('employees:create'))

@login_required       
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zipcode')
        new_employee = Employee(name=name_from_form, user=logged_in_user, zipcode=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.zipcode = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

@login_required
def customerslist(request):
    Customer = apps.get_model('customers.Customer')
    all_customers = Customer.objects.all()
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        today = date.today()
        
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'Customer': all_customers
        }
        return render(request, 'employees/customer_list.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:index'))

@login_required
def customer(request, custid):
    Customer = apps.get_model('customers.Customer')
    mycustomer = Customer.objects.get(id=custid)
    logged_in_user = request.user
    try:
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        today = date.today()
        
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'Customer': mycustomer
        }
        return render(request, 'employees/customerprofile.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:index'))

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from datetime import date
from .models import Employee
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import calendar
from django.db.models import Q

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required 
def index(request):
    Customer = apps.get_model('customers.Customer')
    all_customers = Customer.objects.all()
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
            matched_customers = Customer.objects.filter(zip_code = logged_in_employee.zipcode).filter(Q(weekly_pickup = day) | Q(one_time_pickup = today))
        
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

    if request.method == "POST":
        try:
            # This line will return the customer record of the logged-in user if one exists
            logged_in_employee = Employee.objects.get(user=logged_in_user)
            today = date.today()
            day = calendar.day_name[today.weekday()]

            day_of_week = request.POST.get('day_of_week')
            matched_customers = Customer.objects.filter(weekly_pickup = day_of_week)

            
            context = {
                'logged_in_employee': logged_in_employee,
                'today': today,
                'Customer': all_customers,
                'Customers': matched_customers,
                'day': day
            }
            return render(request, 'employees/customer_list.html', context)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('employees:index'))
    else:
        try:
            # This line will return the customer record of the logged-in user if one exists
            logged_in_employee = Employee.objects.get(user=logged_in_user)
            today = date.today()
            day = calendar.day_name[today.weekday()]
            context = {
                'logged_in_employee': logged_in_employee,
                'today': today,
                'Customer': all_customers,
                'day': day
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
        customer_address = customer_map_profile(mycustomer)
        api_address = f'https://www.google.com/maps/embed/v1/place?key=AIzaSyAU2MXcHftQbhIM7cGPzks9nwmdXecqqkc&q={customer_address}'
        amount = mycustomer.balance
        currency = "${:,.2f}".format(amount)
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'Customer': mycustomer,
            'api_address': api_address,
            'custbalance': currency
        }
        return render(request, 'employees/customerprofile.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:index'))

def customer_map_profile(customer):
    customer_address = customer.address
    customer_zipcode = customer.zip_code

    # Process - replace spaces with '+'
    split_address = customer_address.split()
    formatted_address_no_zip = '+'.join(split_address)
    api_address = formatted_address_no_zip + '+' + customer_zipcode

    return api_address
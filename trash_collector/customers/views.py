from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.conf import settings

from .models import Customer

@login_required
def index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_customer = Customer.objects.get(user=logged_in_user)

        today = date.today()
        todayinteger = date.weekday(today)
        
        context = {
            'logged_in_customer': logged_in_customer,
            'today': today,
            'dayofweek': todayinteger
        }
        return render(request, 'customers/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('customers:create'))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        weekly_from_form = request.POST.get('weekly_pickup')
        new_customer = Customer(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form, weekly_pickup=weekly_from_form)
        new_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/create.html')

@login_required
def suspend_service(request):
    logged_in_user = request.user
    logged_in_customer = Customer.objects.get(user=logged_in_user)
    if request.method == "POST":
        start_from_form = request.POST.get('start')
        end_from_form = request.POST.get('end')
        logged_in_customer.suspend_start = start_from_form
        logged_in_customer.suspend_end = end_from_form
        logged_in_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        context = {
            'logged_in_customer': logged_in_customer
        }
        return render(request, 'customers/suspend.html', context)

@login_required
def one_time_pickup(request):
    logged_in_user = request.user
    logged_in_customer = Customer.objects.get(user=logged_in_user)
    if request.method == "POST":
        date_from_form = request.POST.get('date')
        logged_in_customer.one_time_pickup = date_from_form
        logged_in_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        context = {
            'logged_in_customer': logged_in_customer
        }
        return render(request, 'customers/one_time.html', context)

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_customer = Customer.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        logged_in_customer.name = name_from_form
        logged_in_customer.address = address_from_form
        logged_in_customer.zip_code = zip_from_form
        logged_in_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        context = {
            'logged_in_customer': logged_in_customer
        }
        return render(request, 'customers/edit_profile.html', context)
        
@login_required
def view_that_asks_for_money(request):
    logged_in_user = request.user
    logged_in_customer = Customer.objects.get(user=logged_in_user)
    amount = logged_in_customer.balance
    currency = "${:,.2f}".format(amount)
    host = request.get_host()
    # What you want the button to do.
    paypal_dict = {
        "business": "A & R Trash Services",
        "amount": currency,
        "item_name": "Trash Collection",
        "invoice": "666",
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),

    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render_to_response("payment.html", context)

@csrf_exempt
def payment_done(request):
    return render(request, 'ecommerce_app/payment_done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'ecommerce_app/payment_cancelled.html')

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
        #...
        #...

            cart.clear(request)

            request.session['order_id'] = o.id
            return redirect('process_payment')


    else:
        form = CheckoutForm()
        return render(request, 'ecommerce_app/checkout.html', locals())


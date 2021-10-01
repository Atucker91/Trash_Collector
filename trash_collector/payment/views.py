from django.shortcuts import render
from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import calendar
from django.db.models import Q
from datetime import date
from .models import Employee
from . import views

# # Create your views here.
# def payment_process(request):
#     #order id will be customer id
#     Customer = apps.get_model('customers.Customer')
#     logged_in_user = request.user
#     CustomerPay = Customer.objects.get(user=logged_in_user)
    
#     paypal_dict = {
#         'business':settings.PAYPAL_RECIEVER_EMAIL,
#         'amount': '%.2f' % CustomerPay.balance,
#         'item_name': 'Order {}',
#         'invoice':str(order.id),
#         'currency_code': 'USD',
#         'notify_url': 'http://{}{}'.format(host, reverse('paypal-ip')),
#         'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
#         'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled'))
#     }
#     form = PayPalPaymentsForm(initial=paypal_dict)
    # return render(request, 'payment/process.html')
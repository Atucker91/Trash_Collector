from django.urls import path, include

from . import views

app_name = "customers"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('suspend/', views.suspend_service, name="suspend"),
    path('one_time/', views.one_time_pickup, name="one_time"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('payment/', include("paypal.standard.ipn.urls")),
    path('process-payment/', views.view_that_asks_for_money, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
]

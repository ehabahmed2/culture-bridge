from django.shortcuts import render, redirect
from .forms import CardPaymentForm, VodafonePaymentForm
from django.contrib import messages
# Create your views here.
def plans(request):
    return render(request, 'plans.html', context={})

def payment(request):
    # get the forms from forms.py
    card_form = CardPaymentForm(request.POST or None)
    vodafone_form = VodafonePaymentForm(request.POST or None)

    if request.method == 'POST':
        if 'card_submit' in request.POST and card_form.is_valid():
            # process the card payment
            messages.success(request, "Thanks for the payment, enjoy our service. :)")
            return redirect('payment')
        if 'vodafone_submit' in request.POST and vodafone_form.is_valid():
            # Process vodafone payment
            messages.success(request, "Thanks for the payment, enjoy our service. :)")
            return redirect('payment')
    return render(request, 'fake-payment.html', context={'card_form': card_form, 'vodafone_form': vodafone_form})
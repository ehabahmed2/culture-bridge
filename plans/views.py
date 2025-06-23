from django.shortcuts import render, redirect
from .forms import CardPaymentForm, VodafonePaymentForm
from django.contrib import messages
from dotenv import load_dotenv
import stripe
import os

load_dotenv()



# Create your views here.   
def plans(request):
    return render(request, 'plans.html', context={})

def payment(request):
    # get the forms from forms.py
    card_form = CardPaymentForm(request.POST or None)
    vodafone_form = VodafonePaymentForm(request.POST or None)


    
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method_id')
        credit_amount = request.POST.get('credit_amount')
        price_map = {
            '100': 199,  # $1.99 in cents
            '500': 799   # $7.99 in cents
        }
    
        
        
        try:
            amount = price_map.get(credit_amount, 0)
            if not amount:
                raise ValueError("Invalid credit amount")
            
            stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
            # process the card payment
            payment_intent = stripe.PaymentIntent.create(
                amount= amount,
                currency='usd',
                payment_method=payment_method_id,
                payment_method_types=['card'],
                confirmation_method='automatic',
                confirm=True
            )

            # check if payment went through
            if payment_intent['status'] == 'succeeded':
                messages.success(request, "Thanks for the payment, enjoy our service. :)")
                return redirect('payment_success')
            else: 
                messages.error(request, "Payment failed. Please try again.")
        except Exception as e:
            messages.error(request, f'Payment failed: {str(e)}')
            
        # handle teh vodafone payment
        if 'vodafone_submit' in request.POST and vodafone_form.is_valid():
            # Process vodafone payment
            messages.success(request, "Thanks for the payment, enjoy our service. :)")
            return redirect('payment')
    return render(request, 'fake-payment.html', context={'card_form': card_form, 'vodafone_form': vodafone_form})


def payment_success(request):
    return render(request, 'payment_success.html')

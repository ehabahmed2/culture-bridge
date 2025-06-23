from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator


class CardPaymentForm(forms.Form):
    
    CARD_CHOICES = [
        ('100', '100 Credits - $1.99'),
        ('500', '500 Credits - $7.99 (Best Value)')
    ]
    # create card number field
    card_number = forms.CharField(
        label="Card Number",
        max_length=19,
        required=True,
        validators=[MinLengthValidator(16)],
        widget=forms.TextInput(attrs={
            'placeholder': '4242 4242 4242 4242',
            'class': 'form-control',
            'id': 'cardNumber',
        }))
        #expirey date
    expiry_date = forms.CharField(
        label='Expiry Date', 
        max_length=5, 
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'MM/YY',
            'class': 'form-control'
        }))
    
    cvc = forms.CharField(
        label='CVC',
        max_length=3,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '123',
            'class': 'form-control'
        }))
    card_name = forms.CharField(
        label="Name on Card",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'John Doe',
            'class': 'form-control'
        }))
    credit_amount = forms.ChoiceField(
        label="Credit Amount",
        choices=CARD_CHOICES,
        widget=forms.Select(attrs={'class': 'credit-select'}))
    
class VodafonePaymentForm(forms.Form):
    VODAFONE_CHOICES = [
        ('100', '100 Credits - EGP 30'),
        ('500', '500 Credits - EGP 120 (Best Value)')
    ]
    
    mobile_number = forms.CharField(
        label="Mobile Number",
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '01X-XXXX-XXXX',
            'class': 'form-control'
        })
    )
    pin = forms.CharField(
        label="PIN",
        max_length=4,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': '4-digit PIN',
            'class': 'form-control'
        })
    )
    credit_amount = forms.ChoiceField(
        label="Credit Amount",
        choices=VODAFONE_CHOICES,
        widget=forms.Select(attrs={'class': 'credit-select'})
    )
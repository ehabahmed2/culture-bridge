from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class loginForm(AuthenticationForm):
    # user the email instead of username
    username = forms.CharField(
    widget=forms.TextInput(attrs={
        'class': 'login-input',
        'placeholder': 'Enter your username',
        'id': 'loginEmail',
        'autocomplete': 'username',
    }))
    
    # let the user have this option as a checkbox
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'loginRemember'})
    )
    
    # create the password field then tweek
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({
            'class': 'login-input',
            'placeholder': 'Enter your password',
            'id': 'loginPassword',
            # 'aria-label': 'Toggle password visibility',
        })

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize all fields including password fields
        self.fields['username'].widget.attrs.update({
            'class': 'register-input',
            'id': 'registerUsername',
            'placeholder': 'Enter your username'
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'register-input',
            'id': 'registerEmail',
            'placeholder': 'Enter your email'
        })
        
        self.fields['full_name'].widget.attrs.update({
            'class': 'register-input',
            'id': 'registerFullName',
            'placeholder': 'Enter your full name'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'register-input',
            'id': 'registerPassword',
            'placeholder': 'Create a password'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'register-input',
            'id': 'registerConfirmPassword',
            'placeholder': 'Confirm your password'
        })

class UserUpdate(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize all fields including password fields
        self.fields['username'].widget.attrs.update({
            'class': 'register-input',
            'id': 'registerUsername',
            'placeholder': 'Enter your username'
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'register-input',
            'id': 'registerEmail',
            'placeholder': 'Enter your email'
        })
        
        self.fields['full_name'].widget.attrs.update({
            'class': 'register-input',
            'id': 'registerFullName',
            'placeholder': 'Enter your full name'
        })

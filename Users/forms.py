from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, SetPasswordForm
from .models import CustomUser
from django.utils import timezone

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
    store_history = forms.BooleanField(
        required=False,
        label="Save my translation history",
        widget=forms.CheckboxInput(attrs={
            'class': 'register-checkbox',
            'id':    'store_history',
        })
    )
    
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'password1', 'password2', 'store_history']
        
        
        
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
    
    store_history = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'mr-2',
            'id': 'store_history_setting',
            'onchange': 'return confirmUncheck(this);'  # inline handler
        }),
        label='Store my translation history'
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'store_history']
        
        
        
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


class UpdatePassword(SetPasswordForm):
    """Updating password form"""
    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.fields['new_password1'].widget.attrs.update({
                'class': 'register-input',
                'id': 'id_new_password1',
                'placeholder': 'Enter new password',
                
            })
            self.fields['new_password2'].widget.attrs.update({
                'class': 'register-input',
                'id': 'id_new_password2',
                'placeholder': 'Confirm new password'
            })
            

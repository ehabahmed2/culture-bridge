from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model 
from t_history.models import TransalationHistory
# change from built in user to Custom user 
User = get_user_model()

from .forms import loginForm, RegisterForm, UserUpdate

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', context={'form':form})



def login_user(request):
    if request.method == 'POST':
        form = loginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')  # still called 'username' by Django
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if not form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)  # Expires on browser close
                messages.success(request, f'Welcome {user.username}')
                return redirect('home')  
        else:
            
            messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = loginForm()
    return render(request, 'login.html', {'form': form})



@login_required
# handle issue log out issue with free attempts
def logout_keep_free_attempts(request):
    # 1) grab current tries (default to 10 if missing)
    free = request.session.get('free_attempts', 10)
    
    # 2) perform the normal logout (this *clears* the session)
    logout(request)
    
    #3) restore free attempts into the new empty session
    request.session['free_attempts'] = free
    
    return redirect('home')



@login_required
def user_info(request):
    # get the logged in user
    current_user = User.objects.get(id=request.user.id)
    # get the details from current user and fill it in the form
    user_form = UserUpdate(request.POST or None, instance=current_user) 
    if user_form.is_valid():
        user_form.save()
        login(request, current_user) # to log the user in again after saving info
        messages.success(request, "Your details were saved successfully!")
        return redirect('home')
    
    # get recent transalations for the user
    recent_history = TransalationHistory.objects.filter(user=request.user).order_by('-timestamp')[:3] if request.user.is_authenticated else None
    return render(request, 'user-info.html', {'form': user_form, 'recent_history': recent_history})



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model 
from t_history.models import TransalationHistory
from django.utils import timezone


# change from built in user to Custom user 
User = get_user_model()

from .forms import loginForm, RegisterForm, UserUpdate

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            store_history = form.cleaned_data.get('store_history', False)
            # Create but don’t save yet
            user = form.save(commit=False)
            user.store_history = store_history
            user.consent_date =timezone.now() if store_history else None
            
            # finally save all data 
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
    current_user = request.user
    user_form = UserUpdate(request.POST or None, instance=current_user) 

    if request.method == 'POST':
        # get the details from current user and fill it in the form
        if user_form.is_valid():

            # get the checkout box for concent
            store_history = user_form.cleaned_data.get('store_history', False)
            #save new preference for store history
            current_user.store_history = store_history
            current_user.concent_date = timezone.now() if store_history else None
            
            # if user decided to not approve, delete transalations
            if not store_history:
                TransalationHistory.objects.filter(user=request.user).delete()
            user_form.save()

            messages.success(request, "Your details were saved successfully!")
            return redirect('user_info')
        else: 
            user_form = UserUpdate(request.POST or None, instance=current_user) 

    
    # get recent transalations for the user
    recent_history = TransalationHistory.objects.filter(user=request.user).order_by('-timestamp')[:3] if request.user.is_authenticated else None
    return render(request, 'user-info.html', {'form': user_form, 'recent_history': recent_history})




@login_required
@require_POST
def enable_history_storage(request):
    try:
        request.user.store_history = True
        request.user.consent_date = timezone.now()
        request.user.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

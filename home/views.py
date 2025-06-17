from django.shortcuts import render, redirect
from django.http import JsonResponse
from .transalator.transalator import TranslateEngine  # Relative import
from t_history.models import TransalationHistory
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from Users.models import CustomUser 
from django.db.models import F
from django.contrib.auth import logout as django_logout


import json

def home(request):
    # Initialize free attempts counter for anonymous users
    if not request.user.is_authenticated:
        # Set to 10 if it doesn't exist or is invalid
        if 'free_attempts' not in request.session or not isinstance(request.session['free_attempts'], int):
            request.session['free_attempts'] = 10
    return render(request, 'home.html')

def translate_view(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        dialect = request.POST.get('dialect', 'egyptian')
        
        # Check authentication and credits
        if not request.user.is_authenticated: 
            #handle unauthenticated users
            remaining = request.session.get('free_attempts', 10)
            if remaining <= 0:
                return JsonResponse({
                    'success': False,
                    'error': 'Free limit reached! Please register to continue',
                    'redirect': True
                }, status=403)
        else: 
            # handle authenticated users
            if request.user.credits <= 0:
                return JsonResponse({
                    'success': False,
                    'error': 'No credits left! Please purchase more credits',
                    'redirect': False
                }, status=403)
        
        
        try:
            engine = TranslateEngine()
            translation = engine.translate(text, dialect)
            # Deduct credit/attempt
            
            #deduct attempts from auth users
            if request.user.is_authenticated: 
                CustomUser.objects.filter(pk=request.user.pk).update(credits=F('credits') - 1)
            # Refresh user instance from database
                request.user.refresh_from_db()
                remaining = request.user.credits
            
            # handle unauth users
            else: 
                remaining = request.session.get('free_attempts', 10) - 1
                request.session['free_attempts'] = remaining
            
            # if attempts are not over then proceed
            return JsonResponse({
                'success': True,
                'translation': translation,
                'dialect': dialect,
                'remaining': remaining, 
                'user_authenticated': request.user.is_authenticated,
            })
            
        except Exception as e:
            # Handle specific errors if needed
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
            
    return JsonResponse({'error': 'POST method required'}, status=405)


@login_required
@csrf_exempt
def save_translation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Create and save history entry
            TransalationHistory.objects.create(
                user=request.user,
                input_text=data['input_text'],
                output_text=data['output_text'],
                target_culture=data['target_culture']
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)


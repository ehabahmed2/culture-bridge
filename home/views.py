from django.shortcuts import render
from django.http import JsonResponse
from .transalator.transalator import TranslateEngine  # Relative import
from t_history.models import TransalationHistory
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import json

# Create your views here.
def home(request):
    return render(request, 'home.html', context={})

def translate_view(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        dialect = request.POST.get('dialect', 'egyptian')
        
        try:
            engine = TranslateEngine()
            translation = engine.translate(text, dialect)
            return JsonResponse({
                'success': True,
                'translation': translation,
                'dialect': dialect
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

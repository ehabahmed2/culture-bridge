from django.shortcuts import render
from django.http import JsonResponse
from .transalator.transalator import TranslateEngine  # Relative import

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

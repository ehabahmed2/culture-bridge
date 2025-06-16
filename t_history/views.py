from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TransalationHistory
from django.contrib import messages

from django.shortcuts import redirect, get_object_or_404




# Create your views here.
@login_required
def translation_history(request):
    # get the user's history ordered by most recent
    history = TransalationHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'history.html', context={'history': history})


@login_required
def delete_history(request):
    if request.method == 'POST':
        if 'entry_id' in request.POST:
            entry_id = request.POST['entry_id']
            entry = get_object_or_404(TransalationHistory, id=entry_id, user=request.user)
            entry.delete()
            messages.success(request, 'Translation deleted successfully!')
        elif request.POST.get('delete_all') == 'true':
            TransalationHistory.objects.filter(user=request.user).delete()
            messages.success(request, 'All translation history deleted')
    return redirect('history')


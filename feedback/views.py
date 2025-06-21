from django.shortcuts import render

# Create your views here.
def feedback(request):
    return render(request, 'feedback.html',context={})
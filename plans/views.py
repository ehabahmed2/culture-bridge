from django.shortcuts import render

# Create your views here.
def plans(request):
    return render(request, 'plans.html', context={})


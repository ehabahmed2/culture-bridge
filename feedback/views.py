import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.sessions.models import Session
from .forms import FeedbackFrom

def feedback(request):
    # 1) Handle AJAX POST with JSON
    if request.method == "POST" and request.content_type == "application/json":
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

        # 2) You can either use the ModelForm...
        form = FeedbackFrom(payload)
        # ...or skip the form and construct the model directly.
        if form.is_valid():
            fb = form.save(commit=False)

            # 3) Attach user if authenticated
            if request.user.is_authenticated:
                fb.user = request.user
            else:
                fb.user = None

            # 4) Look up the Session object by key (or set to None)
            session_key = payload.get("session_key") or request.session.session_key
            try:
                fb.session = Session.objects.get(session_key=session_key)
            except Session.DoesNotExist:
                fb.session = None

            # 5) Save it
            fb.save()

            # 6) Return success back to JS
            messages.success(request, 'Thanks for the feedback')

            return JsonResponse({"success": True})

        # Form was invalid
        return JsonResponse({"success": False, "errors": form.errors}, status=400)


# 2) Handle *normal* POST from the standalone form
    if request.method == "POST":
        form = FeedbackFrom(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.user = request.user if request.user.is_authenticated else None
            # Associate session if you like, or skip:
            try:
                fb.session = Session.objects.get(session_key=request.session.session_key)
            except Session.DoesNotExist:
                fb.session = None
            fb.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect("feedback")  # or wherever you want to go


    else: 
        #7) If it’s a regular GET, render the page with the ModelForm
        form = FeedbackFrom()
    return render(request, "feedback.html", {"form": form})




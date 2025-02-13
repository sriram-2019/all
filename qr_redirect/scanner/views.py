from django.shortcuts import redirect
from django.http import HttpRequest

def qr_redirect(request: HttpRequest):
    user_agent = request.headers.get('User-Agent', '').lower()

    if "kivyapp" in user_agent:  # If scanned from Kivy app
        return redirect("https://fb.com")  # Redirect to Facebook
    else:  # Any other app
        return redirect("https://google.com")  # Redirect to Google

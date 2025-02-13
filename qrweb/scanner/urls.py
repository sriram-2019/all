from django.urls import path
from .views import qr_scanner, qr_redirect

urlpatterns = [
    path("", qr_scanner, name="qr_scanner"),
    path("redirect/", qr_redirect, name="qr_redirect"),
]

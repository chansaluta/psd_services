from django.urls import path
from apps.rrptp_server.views import *



urlpatterns = [
    path('', index, name='rrptp_page' ),
    path('dashboard/', dashboard, name='dashboard' ),
]

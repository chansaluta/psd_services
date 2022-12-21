from django.urls import path
from apps.mta_server.views import *



urlpatterns = [
    path('', index, name='mta_page' ),
    
]

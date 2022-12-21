from django.urls import path
from apps.sfp_server.views import *



urlpatterns = [
    path('', index, name='sfp_page' ),
     path('dashboard/', dashboard, name='dashboard' ),
]

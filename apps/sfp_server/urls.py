from django.urls import path
from apps.sfp_server.views import *



urlpatterns = [
    path('', index, name='sfp_page' ),
    path('dashboard/', dashboard, name='sfp_dashboard' ),
    # ! Status Tool Directory Path
    path('status_tool/', nut_status_add_data, name='nut_status_add_data'),

    # ! Children Status Directory Path
    path('children_status/underweight/', underweight_children, name='underweight_children' ),
    path('children_status/stunted/', stunted_children, name='stunted_children' ),
    path('children_status/moderately_wasted/', moderately_wasted_children, name='moderately_wasted_children' ),
    path('children_status/severely_underweight/', severely_underweight_children, name='severely_underweight_children' ),
    path('children_status/severely_stunted/', severely_stunted_children, name='severely_stunted_children'  ),
    path('children_status/severely_wasted/', severely_wasted_children, name='severely_wasted_children' ),
    
    path('summary/', summary, name='summary')
    


]

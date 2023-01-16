from django.urls import path
from apps.outpass_locator.views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('dashboard/', dashboard, name='dashboard' ),

    path('monitoring/all_outpass_logs/', all_outpass_logs, name='all_outpass_logs' ),
    path('monitoring/today_outpass_logs/', today_outpass_logs, name='today_outpass_logs' ),

    path('monitoring/staff_details/', staff_details, name='staff_details' ),
    path('monitoring/staff_program/', staff_program, name='staff_program' ),
    path('monitoring/tracker/', tracker, name='tracker' ),

    path('administrator/registration/', registration, name='registration' ),


    path('administrator/ajax/employee_list/<str:key>/', employee_list, name='employee_list' ),

    path('administrator/register_outpass_account/', register_outpass_account, name='register_outpass_account'),

    path('ajax/get_all_staff_details/', get_all_staff_details, name='get_all_staff_details'),

    path('ajax/get_staff_details_by_program/', get_staff_details_by_program, name='get_staff_details_by_program'),
    

    path('ajax/get_staff_outpass_logs/', get_staff_outpass_logs, name='get_staff_outpass_logs'),

    path('ajax/get_staff_outpass_today_logs/', get_staff_outpass_today_logs, name='get_staff_outpass_today_logs'),

    path('ajax/staff_status_update/<pk>/', staff_status_update, name='staff_status_update'),

    path('ajax/update_staff_status/', update_staff_status, name='update_staff_status'),
    

    path('', login_user, name='login_user'),
    path('logout/', logout_user, name='logout'),
    
    

    path('administrator/scan_qr_outpass/<str:id_number>/', scan_qr_outpass, name='scan_qr_outpass'),

   
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root =settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
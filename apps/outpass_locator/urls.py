from django.urls import path
from apps.outpass_locator.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard' ),

    path('monitoring/all_outpass_logs/', all_outpass_logs, name='all_outpass_logs' ),
    path('monitoring/today_outpass_logs/', today_outpass_logs, name='today_outpass_logs' ),
    path('monitoring/program_outpass_logs/', program_outpass_logs, name='program_outpass_logs'),

    path('monitoring/staff_details/', staff_details, name='staff_details' ),
    path('monitoring/staff_program/', staff_program, name='staff_program' ),
    path('monitoring/tracker/', tracker, name='tracker' ),

    path('administrator/registration/', registration, name='registration' ),


    path('administrator/ajax/employee_list/<str:key>/', employee_list, name='employee_list' ),

    path('administrator/register_outpass_account/', register_outpass_account, name='register_outpass_account'),

    path('ajax/get_all_staff_details/', get_all_staff_details, name='get_all_staff_details'),

    path('ajax/get_staff_details_by_program/', get_staff_details_by_program, name='get_staff_details_by_program'),
    

    path('ajax/get_staff_personal_outpass_logs/', get_staff_personal_outpass_logs, name='get_staff_personal_outpass_logs'),

    path('ajax/get_staff_personal_outpass_today_logs/', get_staff_personal_outpass_today_logs, name='get_staff_personal_outpass_today_logs'),

    path('ajax/get_staff_official_outpass_logs/', get_staff_official_outpass_logs, name='get_staff_official_outpass_logs'),

    path('ajax/get_staff_official_outpass_today_logs/', get_staff_official_outpass_today_logs, name='get_staff_official_outpass_today_logs'),

    path('ajax/staff_status_update/<pk>/', staff_status_update, name='staff_status_update'),

    path('ajax/update_staff_status/', update_staff_status, name='update_staff_status'),

    path('ajax/get_personal_outpass_leaderboard/', get_personal_outpass_leaderboard, name='get_personal_outpass_leaderboard'),

    path('ajax/program_official_outpass_logs/', program_official_outpass_logs, name='program_official_outpass_logs'),

    path('ajax/program_personal_outpass_logs/', program_personal_outpass_logs, name='program_personal_outpass_logs'),   

    path('ajax/get_official_outpass_leaderboard/', get_official_outpass_leaderboard, name='get_official_outpass_leaderboard'),   

    # path('download_staff_qr_code/<id>/', download_staff_qr_code, name='download_staff_qr_code'),

    path('outpass_approved_action/', outpass_approved_action, name='outpass_approved_action'), 

    path('update_remarks_official_outpass/', update_remarks_official_outpass, name='update_remarks_official_outpass'),
    path('view_remarks_official/<pk>/', view_remarks_official, name='view_remarks_official'),

    path('print_outpass/', print_staff_outpass, name='print_staff_outpass'),

    

    
    
    
    

    path('', login_user, name='login_user'),
    path('logout/', logout_user, name='logout'),
    
    

    path('administrator/scan_qr_outpass/<str:id_number>/', scan_qr_outpass, name='scan_qr_outpass'),

    path('outpass_approved', outpass_approved, name='outpass_approved'),

    path('download/<path>/', serve, {'document_root': settings.MEDIA_ROOT}),

   
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root =settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
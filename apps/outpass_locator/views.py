from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from apps.outpass_locator.models import *
from time import  strftime
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import connection

from itertools import chain
from django.conf import settings

date_today = strftime("%m/%d/%Y")


import time
api_employee_url_any = 'https://caraga-portal.dswd.gov.ph/api/employee/list/search/?q='
api_headers = {'Authorization': 'Token 83b68c4f61f9642cf22a9de910e4369d7d051ff5'}

# Create your views here.

# ! Frontend


@login_required
def dashboard(request):
    template = "app/pages/dashboard.html"
    active_staff = outpass_locator_staff_details.objects.all().count()
    on_leave_staff = outpass_locator_staff_details.objects.filter(status=6).count()
    staff_use_outpass = outpass_locator_staff_details.objects.filter(status=3).count()

    count_outpass = outpass_locator_logs.objects.values('id_number','user_id').annotate(Count('user_id')).order_by()

    context = {
        'active_user': active_staff,
        'staff_use_outpass': staff_use_outpass,
        'on_leave_staff': on_leave_staff,
        'count_outpass': count_outpass

    }

    return render(request, template, context)


@login_required
def all_outpass_logs(request):
    template = "app/pages/outpass_logs/all_outpass_logs.html"
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, template)

    return redirect('dashboard')

    

    

@login_required
def today_outpass_logs(request):
    template = "app/pages/outpass_logs/today_outpass_logs.html"
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, template)

    return redirect('dashboard')


@login_required
def staff_details(request):
    template = "app/pages/monitoring/staff_details.html"
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, template)

    return redirect('dashboard')

@login_required
def staff_program(request):
    template = "app/pages/monitoring/staff_program.html"

    return render(request, template)


@login_required
def program_outpass_logs(request):
    template = "app/pages/outpass_logs/by_program_outpass_logs.html"
    user = request.user.id

    program = outpass_locator_staff_details.objects.filter(auth_user_id=user)

    for prog in program:
        user_program = prog.program


    context = {
        'user_program': user_program
    }
  


    return render(request,template, context)

@login_required
def tracker(request):
    template = "app/pages/monitoring/tracker.html"

    secretariat_staff = outpass_locator_staff_details.objects.filter(outpass_locator_program_id=1).order_by('-id')
    mta_staff = outpass_locator_staff_details.objects.filter(outpass_locator_program_id=2)
    arrs_staff = outpass_locator_staff_details.objects.filter(outpass_locator_program_id=3).order_by('-id')
    sectoral_staff = outpass_locator_staff_details.objects.filter(outpass_locator_program_id=4).order_by('first_name')
    cbu_staff = outpass_locator_staff_details.objects.filter(outpass_locator_program_id=5).order_by('first_name')
    rrptp_staff = outpass_locator_staff_details.objects.filter(outpass_locator_program_id=6).order_by('last_name')
    socpen_staff = outpass_locator_staff_details.objects.filter(outpass_locator_program_id=7).order_by('id')
    sfp_staff = outpass_locator_staff_details.objects.filter(outpass_locator_program_id=8).order_by('last_name')
    cis_staff = outpass_locator_staff_details.objects.filter(outpass_locator_program_id=9)

    context = {
        'secretariat_staff': secretariat_staff,
        'mta_staff': mta_staff,
        'arrs_staff': arrs_staff,
        'sectoral_staff': sectoral_staff,
        'cbu_staff': cbu_staff,
        'rrptp_staff': rrptp_staff,
        'sfp_staff': sfp_staff,
        'socpen_staff': socpen_staff,
        'cis_staff': cis_staff
    }

    return render(request, template, context)

@login_required
def registration(request):
    template = "app/pages/administrator/registration.html"

    return render(request, template)

# ! Backend

@login_required
def employee_list(request,key):
    if key is not None:
        response = requests.get( api_employee_url_any + key, headers=api_headers)
    
        todos = response.json()

        data = dict()
        data['todos'] = todos

    return JsonResponse(data, safe=False)


@login_required
def register_outpass_account(request):
    
    if request.method == "POST":
        pass_word = request.POST.get('id_number')
        encrypt_pass = make_password(pass_word)
        
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')

        fullname = firstname + ' ' + middlename[1] + ' ' + lastname
    
    auth_user_register = User(
        username = request.POST.get('username'),
        is_superuser = 0,
        password = encrypt_pass,
        first_name = request.POST.get('firstname'),
        last_name = request.POST.get('lastname'),
        email = request.POST.get('email'),
        is_staff = 1,
        is_active = 0,
    )
    auth_user_register.save()

    staff_registration_outpass = outpass_locator_staff_details(

        auth_user_id    =   auth_user_register.id,
        id_number = request.POST.get('id_number'),
        first_name = request.POST.get('firstname'),
        middle_name = request.POST.get('middlename'),
        last_name = request.POST.get('lastname'),
        ext_name = request.POST.get('extension'),
        full_name = fullname,
        position = request.POST.get('position'),
        status = 1,
        program =  request.POST.get('section'),
        current_personal_outpass_id = 0,
        current_official_outpass_id = 0
    )
    staff_registration_outpass.save()

    return redirect('registration')


@login_required
def get_all_staff_details(request):

    all_staff_details = outpass_locator_staff_details.objects.all().extra(
        select = {'id': 'outpass_locator_staff_details.id', 'id_number': 'outpass_locator_staff_details.id_number' , 'first_name': 'outpass_locator_staff_details.first_name', 
        'middle_name': 'outpass_locator_staff_details.middle_name', 'last_name': 'outpass_locator_staff_details.last_name', 'ext_name': 'outpass_locator_staff_details.ext_name',
        'position': 'outpass_locator_staff_details.position', 'status': 'outpass_locator_staff_details.status', 'program': 'outpass_locator_staff_details.program', 'username': 'auth_user.username',
        'email': 'auth_user.email', 'image': 'outpass_locator_staff_details.image'},
        tables= ['auth_user', 'outpass_locator_staff_details'],
        where=[ 'outpass_locator_staff_details.auth_user_id = auth_user.id' ]

    )
    all_staff_details_list = list(all_staff_details.values('id','id_number','first_name','middle_name','last_name','ext_name','position','status','program','username','email','image'))

    data = {
        'data': all_staff_details_list
    }

    return JsonResponse(data)






@login_required
def get_staff_personal_outpass_logs(request):

    staff_personal_outpass_logs = outpass_locator_logs.objects.all().extra(
        select = {'id': 'outpass_locator_logs.id','first_name': 'outpass_locator_staff_details.first_name', 'middle_name': 'outpass_locator_staff_details.middle_name', 'last_name': 'outpass_locator_staff_details.last_name',
        'position': 'outpass_locator_staff_details.position', 'image': 'outpass_locator_staff_details.image', 'program': 'outpass_locator_staff_details.program','inclusive_dates': 'outpass_locator_logs.inclusive_dates',
        'time_check_out': 'outpass_locator_logs.time_check_out', 'time_check_in': 'outpass_locator_logs.time_check_in', 'time_span_outpass': 'outpass_locator_logs.time_span_outpass', 
        'status': 'outpass_locator_staff_details.status', 'month': 'outpass_locator_logs.month', 'full_name': 'outpass_locator_staff_details.full_name'},
        tables=['outpass_locator_logs', 'outpass_locator_staff_details'],
        where=['outpass_locator_logs.outpass_locator_staff_details_id = outpass_locator_staff_details.id']
    )

    staff_personal_outpass_logs_data = list(staff_personal_outpass_logs.values('full_name','month','first_name','middle_name','last_name','position','image','program','inclusive_dates','time_check_out','time_check_in','time_span_outpass','status','id'))

    data = {
        'data': staff_personal_outpass_logs_data
    }

    return JsonResponse(data)



@login_required
def get_staff_personal_outpass_today_logs(request):

    staff_personal_outpass_today_logs = outpass_locator_logs.objects.all().extra(
        select = {'id': 'outpass_locator_logs.id','first_name': 'outpass_locator_staff_details.first_name', 'middle_name': 'outpass_locator_staff_details.middle_name', 'last_name': 'outpass_locator_staff_details.last_name',
        'position': 'outpass_locator_staff_details.position', 'image': 'outpass_locator_staff_details.image', 'program': 'outpass_locator_staff_details.program','inclusive_dates': 'outpass_locator_logs.inclusive_dates',
        'time_check_out': 'outpass_locator_logs.time_check_out', 'time_check_in': 'outpass_locator_logs.time_check_in', 'time_span_outpass': 'outpass_locator_logs.time_span_outpass', 
        'status': 'outpass_locator_staff_details.status', 'full_name': 'outpass_locator_staff_details.full_name'},
        tables=['outpass_locator_logs', 'outpass_locator_staff_details'],
        where=['outpass_locator_logs.outpass_locator_staff_details_id = outpass_locator_staff_details.id', 'outpass_locator_logs.inclusive_dates = "' +date_today+ '"']
    )

    staff_personal_outpass_today_logs_data = list(staff_personal_outpass_today_logs.values('full_name','first_name','middle_name','last_name','position','image','program','inclusive_dates','time_check_out','time_check_in','time_span_outpass','status','id'))

    data = {
        'data': staff_personal_outpass_today_logs_data
    }

    return JsonResponse(data)






## * Login Query
def login_user(request):
    template = "app/index.html"
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.INFO, 'Username or Password is incorrect!')
            return redirect('login_user')

    else:
        return render(request,template, {})

## * Logout Query
def logout_user(request):
	logout(request)
	return redirect('login_user')




@login_required
def get_staff_details_by_program(request):

    user = request.user.id

    user_program = outpass_locator_staff_details.objects.filter(auth_user_id=user)

    for instance in user_program:
        program = instance.program

    all_staff_details = outpass_locator_staff_details.objects.all().extra(
        select = {'id': 'outpass_locator_staff_details.id', 'id_number': 'outpass_locator_staff_details.id_number' , 'first_name': 'outpass_locator_staff_details.first_name', 
        'middle_name': 'outpass_locator_staff_details.middle_name', 'last_name': 'outpass_locator_staff_details.last_name', 'ext_name': 'outpass_locator_staff_details.ext_name',
        'position': 'outpass_locator_staff_details.position', 'status': 'outpass_locator_staff_details.status', 'program': 'outpass_locator_staff_details.program', 'username': 'auth_user.username',
        'email': 'auth_user.email', 'image': 'outpass_locator_staff_details.image'},
        tables= ['auth_user', 'outpass_locator_staff_details'],
        where=[ 'outpass_locator_staff_details.auth_user_id = auth_user.id', 'outpass_locator_staff_details.program = "' + program + '"' ]

    )
    all_staff_details_list = list(all_staff_details.values('id','id_number','first_name','middle_name','last_name','ext_name','position','status','program','username','email','image','qr_code'))

    data = {
        'data': all_staff_details_list
    }

    return JsonResponse(data)


@login_required
def staff_status_update(request,pk):

    if pk is not None:

        status = outpass_locator_staff_details.objects.all().extra(
            select = {'id': 'outpass_locator_staff_details.id','first_name': 'outpass_locator_staff_details.first_name', 'middle_name': 'outpass_locator_staff_details.middle_name', 'last_name': 'outpass_locator_staff_details.last_name',
            'id_number': 'outpass_locator_staff_details.id_number', 'position': 'outpass_locator_staff_details.position', 'status': 'outpass_locator_staff_details.status'},
            tables = ['outpass_locator_staff_details'],
            where = ['outpass_locator_staff_details.id = '+ pk],
        )

        status_modal_data = list(status.values('first_name','middle_name','last_name','id_number','position','status', 'id'))
        data = dict()
        data['status_modal_data'] = status_modal_data

    return JsonResponse(data, safe=False)


@login_required
def update_staff_status(request):

    if request.method == "POST":
        id = request.POST.get('staff_id')
        status = request.POST.get('staff_status')
        status_query = get_object_or_404(outpass_locator_staff_details,id=id)
        status_query.status = status
        status_query.save()

    return redirect('staff_program')

@login_required
def get_personal_outpass_leaderboard(request):

    count_outpass_per_staff = ('SELECT  image , full_name, outpass_locator_logs.id_number, count(user_id) as outpass_count from outpass_locator_logs INNER JOIN outpass_locator_staff_details '+
    'ON outpass_locator_staff_details.auth_user_id = outpass_locator_logs.user_id '+
    'GROUP BY outpass_locator_logs.id_number, outpass_locator_staff_details.image,  outpass_locator_staff_details.full_name ORDER BY count(user_id) DESC LIMIT 5')

    array_list = []
    
    cursor = connection.cursor()
    cursor.execute(count_outpass_per_staff)
    result = cursor.fetchall()
    connection.commit()
    
    for row in result:
        outpass_data = ({
            'image': row[0],
            'full_name': row[1],
            'id_number': row[2],
            'outpass_count': row[3]
        })

        array_list.append(outpass_data)

    return JsonResponse(array_list,safe=False)


@login_required
def get_official_outpass_leaderboard(request):

    count_outpass_per_staff = ('SELECT  image , full_name, official_outpass_locator_logs.id_number, count(user_id) as outpass_count from official_outpass_locator_logs INNER JOIN outpass_locator_staff_details '+
    'ON outpass_locator_staff_details.auth_user_id = official_outpass_locator_logs.user_id '+
    'GROUP BY official_outpass_locator_logs.id_number, outpass_locator_staff_details.image,  outpass_locator_staff_details.full_name ORDER BY count(user_id) DESC LIMIT 5')

    array_list = []
    
    cursor = connection.cursor()
    cursor.execute(count_outpass_per_staff)
    result = cursor.fetchall()
    connection.commit()
    
    for row in result:
        outpass_data = ({
            'image': row[0],
            'full_name': row[1],
            'id_number': row[2],
            'outpass_count': row[3]
        })

        array_list.append(outpass_data)

    return JsonResponse(array_list,safe=False)




@login_required
def outpass_approved(request):

    if request.method == "POST":
        
        outpass_type_id = request.POST.get('outpass_type')
        staff_details_id = request.POST.get('staff_id')
        staff_details = outpass_locator_staff_details.objects.filter(id=staff_details_id)
        for staff in staff_details:
                id_number = staff.id_number
                status = staff.status
                auth_user_id = staff.auth_user_id
                id = staff.id
                
                # ! If Outpass Type is Official
                if outpass_type_id == '1' and status == 1:
                    outpass_locator_staff_details.objects.filter(id=id).update(status=2)
                    insert_official_outpass = official_outpass_locator_logs(
                        id_number                           =   id_number,
                        user_id                             =   auth_user_id,
                        outpass_locator_staff_details_id    =   id,
                        remarks                             =   request.POST.get('remarks'),
                        place_visited                       =   request.POST.get('destination'),
                        if_approved                         =   0
                    )
                    insert_official_outpass.save()
                    outpass_locator_staff_details.objects.filter(id=id).update(current_official_outpass_id=insert_official_outpass.id)
                
                # ! If Outpass Type is Personal
                elif outpass_type_id == '2' and status == 1:
                    outpass_locator_staff_details.objects.filter(id=id).update(status=2)
                    insert_personal_outpass = outpass_locator_logs(
                        id_number                           =   id_number,
                        user_id                             =   auth_user_id,
                        outpass_locator_staff_details_id    =   id,
                        if_approved                         =   0
                    )
                    insert_personal_outpass.save()
                    outpass_locator_staff_details.objects.filter(id=id).update(current_personal_outpass_id=insert_personal_outpass.id)

            
    return redirect('staff_program')

    
    
@login_required
def scan_qr_outpass(request,id_number=None):
    template = "app/pages/monitoring/tracker.html"
    if id_number is not None:

        month_today = datetime.now()
        months = ['zero','January','February','March','April','May','June','July','August','September','October','November','December']
        current_month = months[month_today.month]
        
        qr_staff = outpass_locator_staff_details.objects.filter(id_number=id_number)
        current_date = strftime("%m/%d/%Y")
        t = time.localtime()
        current_time = time.strftime("%I:%M", t)
        timeformat = '%I:%M'
    for instance in qr_staff:
        status = instance.status
        id = instance.id
        official = instance.current_official_outpass_id
        personal = instance.current_personal_outpass_id

        # * Approved Entry Official Outpass (Check Out)
        if status == 2 and personal == 0 and official != 0:
            outpass_locator_staff_details.objects.filter(id=id).update(status=3)
            official_outpass_locator_logs.objects.filter(id=official).update(
                inclusive_dates         =           current_date,
                time_check_out          =           current_time,
                if_approved             =           1,
                month                   =           current_month      
            )
        
        # * Approved Entry Personal Outpass (Check Out)
        elif status == 2 and official == 0 and personal != 0:
            outpass_locator_staff_details.objects.filter(id=id).update(status=3)
            outpass_locator_logs.objects.filter(id=personal).update(
                inclusive_dates         =           current_date,
                time_check_out          =           current_time,
                if_approved             =           1,
                month                   =           current_month 
            )
        
        # * Approved Entry Official Outpass (Check In)
        elif status == 3 and personal == 0 and official != 0:
            official_outpass_locator_data = official_outpass_locator_logs.objects.filter(id=official)
            for official_outpass_data in official_outpass_locator_data:
                official_check_out = official_outpass_data.time_check_out
                official_time_used = datetime.strptime(current_time, timeformat) - datetime.strptime(official_check_out, timeformat)
                official_outpass_locator_logs.objects.filter(id=official).update(time_check_in=current_time)
                official_outpass_locator_logs.objects.filter(id=official).update(time_span_outpass=official_time_used)

                outpass_locator_staff_details.objects.filter(id=id).update(current_official_outpass_id=0)
                outpass_locator_staff_details.objects.filter(id=id).update(status=1)

        
        # * Approved Entry Personal Outpass (Check In)
        elif status == 3 and official == 0 and personal != 0:
            personal_outpass_locator_data = outpass_locator_logs.objects.filter(id=personal)
            for personal_outpass_data in personal_outpass_locator_data:
                personal_check_out = personal_outpass_data.time_check_out
                personal_time_used = datetime.strptime(current_time, timeformat) - datetime.strptime(personal_check_out, timeformat)
                outpass_locator_logs.objects.filter(id=personal).update(time_check_in=current_time)
                outpass_locator_logs.objects.filter(id=personal).update(time_span_outpass=personal_time_used)

                outpass_locator_staff_details.objects.filter(id=id).update(current_personal_outpass_id=0)
                outpass_locator_staff_details.objects.filter(id=id).update(status=1)

        

        # * IF Staff is on RSO
        elif status == 4 and personal == 0 and official == 0:
            messages.error(request, 'Staff is on RSO!')
        

        # * IF Staff is on Travel
        elif status == 5 and personal == 0 and official == 0:
            messages.error(request, 'Staff is on Travel!')
        

        # * IF Staff is on Leave
        elif status == 6 and personal == 0 and official == 0:
            messages.error(request, 'Staff is on Leave!')




        return render(request,template)




@login_required
def get_staff_official_outpass_logs(request):

    staff_official_outpass_logs = official_outpass_locator_logs.objects.all().extra(
        select = {'id': 'official_outpass_locator_logs.id','first_name': 'outpass_locator_staff_details.first_name', 'middle_name': 'outpass_locator_staff_details.middle_name', 'last_name': 'outpass_locator_staff_details.last_name',
        'position': 'outpass_locator_staff_details.position', 'image': 'outpass_locator_staff_details.image', 'program': 'outpass_locator_staff_details.program','inclusive_dates': 'official_outpass_locator_logs.inclusive_dates',
        'time_check_out': 'official_outpass_locator_logs.time_check_out', 'time_check_in': 'official_outpass_locator_logs.time_check_in', 'time_span_outpass': 'official_outpass_locator_logs.time_span_outpass', 
        'status': 'outpass_locator_staff_details.status', 'month': 'official_outpass_locator_logs.month', 'full_name': 'outpass_locator_staff_details.full_name', 'remarks': 'official_outpass_locator_logs.remarks',
        'destination': 'official_outpass_locator_logs.place_visited'},
        tables=['official_outpass_locator_logs', 'outpass_locator_staff_details'],
        where=['official_outpass_locator_logs.outpass_locator_staff_details_id = outpass_locator_staff_details.id']
    )

    staff_officla_outpass_logs_data = list(staff_official_outpass_logs.values('full_name','month','first_name','middle_name','last_name','position','image','program','inclusive_dates','time_check_out','time_check_in','time_span_outpass',
    'status','id','remarks','destination'))

    data = {
        'data': staff_officla_outpass_logs_data
    }

    return JsonResponse(data)



@login_required
def get_staff_official_outpass_today_logs(request):

    staff_official_outpass_today_logs = official_outpass_locator_logs.objects.all().extra(
        select = {'id': 'official_outpass_locator_logs.id','first_name': 'outpass_locator_staff_details.first_name', 'middle_name': 'outpass_locator_staff_details.middle_name', 'last_name': 'outpass_locator_staff_details.last_name',
        'position': 'outpass_locator_staff_details.position', 'image': 'outpass_locator_staff_details.image', 'program': 'outpass_locator_staff_details.program','inclusive_dates': 'official_outpass_locator_logs.inclusive_dates',
        'time_check_out': 'official_outpass_locator_logs.time_check_out', 'time_check_in': 'official_outpass_locator_logs.time_check_in', 'time_span_outpass': 'official_outpass_locator_logs.time_span_outpass', 
        'status': 'outpass_locator_staff_details.status', 'full_name': 'outpass_locator_staff_details.full_name', 'remarks': 'official_outpass_locator_logs.remarks',
        'destination': 'official_outpass_locator_logs.place_visited'},
        tables=['official_outpass_locator_logs', 'outpass_locator_staff_details'],
        where=['official_outpass_locator_logs.outpass_locator_staff_details_id = outpass_locator_staff_details.id', 'official_outpass_locator_logs.inclusive_dates = "' +date_today+ '"']
    )

    staff_official_outpass_today_logs_data = list(staff_official_outpass_today_logs.values('full_name','first_name','middle_name','last_name','position','image','program','inclusive_dates','time_check_out','time_check_in','time_span_outpass'
    ,'status','id','remarks','destination'))

    data = {
        'data': staff_official_outpass_today_logs_data
    }

    return JsonResponse(data)




@login_required
def program_official_outpass_logs(request):
    
    user = request.user.id

    user_program = outpass_locator_staff_details.objects.filter(auth_user_id=user)

    for instance in user_program:
        program = instance.program  

    staff_official_outpass_logs = official_outpass_locator_logs.objects.all().extra(
        select = {'id': 'official_outpass_locator_logs.id','first_name': 'outpass_locator_staff_details.first_name', 'middle_name': 'outpass_locator_staff_details.middle_name', 'last_name': 'outpass_locator_staff_details.last_name',
        'position': 'outpass_locator_staff_details.position', 'image': 'outpass_locator_staff_details.image', 'program': 'outpass_locator_staff_details.program','inclusive_dates': 'official_outpass_locator_logs.inclusive_dates',
        'time_check_out': 'official_outpass_locator_logs.time_check_out', 'time_check_in': 'official_outpass_locator_logs.time_check_in', 'time_span_outpass': 'official_outpass_locator_logs.time_span_outpass', 
        'status': 'outpass_locator_staff_details.status', 'month': 'official_outpass_locator_logs.month', 'full_name': 'outpass_locator_staff_details.full_name', 'remarks': 'official_outpass_locator_logs.remarks',
        'destination': 'official_outpass_locator_logs.place_visited','user_id': 'official_outpass_locator_logs.user_id'},
        tables=['official_outpass_locator_logs', 'outpass_locator_staff_details'],
        where=['official_outpass_locator_logs.outpass_locator_staff_details_id = outpass_locator_staff_details.id',  'outpass_locator_staff_details.program = "' + program + '"' ]
    )

    staff_officla_outpass_logs_data = list(staff_official_outpass_logs.values('full_name','month','first_name','middle_name','last_name','position','image','program','inclusive_dates','time_check_out','time_check_in','time_span_outpass',
    'status','id','remarks','destination','user_id'))

    data = {
        'data': staff_officla_outpass_logs_data
    }

    return JsonResponse(data)





@login_required
def program_personal_outpass_logs(request):

    user = request.user.id

    user_program = outpass_locator_staff_details.objects.filter(auth_user_id=user)

    for instance in user_program:
        program = instance.program  

    staff_personal_outpass_logs = outpass_locator_logs.objects.all().extra(
        select = {'id': 'outpass_locator_logs.id','first_name': 'outpass_locator_staff_details.first_name', 'middle_name': 'outpass_locator_staff_details.middle_name', 'last_name': 'outpass_locator_staff_details.last_name',
        'position': 'outpass_locator_staff_details.position', 'image': 'outpass_locator_staff_details.image', 'program': 'outpass_locator_staff_details.program','inclusive_dates': 'outpass_locator_logs.inclusive_dates',
        'time_check_out': 'outpass_locator_logs.time_check_out', 'time_check_in': 'outpass_locator_logs.time_check_in', 'time_span_outpass': 'outpass_locator_logs.time_span_outpass', 
        'status': 'outpass_locator_staff_details.status', 'month': 'outpass_locator_logs.month', 'full_name': 'outpass_locator_staff_details.full_name'},
        tables=['outpass_locator_logs', 'outpass_locator_staff_details'],
        where=['outpass_locator_logs.outpass_locator_staff_details_id = outpass_locator_staff_details.id',   'outpass_locator_staff_details.program = "' + program + '"']
    )

    staff_personal_outpass_logs_data = list(staff_personal_outpass_logs.values('full_name','month','first_name','middle_name','last_name','position','image','program','inclusive_dates','time_check_out','time_check_in','time_span_outpass','status','id'))

    data = {
        'data': staff_personal_outpass_logs_data
    }

    return JsonResponse(data)


@login_required
def outpass_approved_action(request):

    id_number = request.POST.get('id_number')

    if id_number is not None:

        month_today = datetime.now()
        months = ['zero','January','February','March','April','May','June','July','August','September','October','November','December']
        current_month = months[month_today.month]
        
        qr_staff = outpass_locator_staff_details.objects.filter(id_number=id_number)
        current_date = strftime("%m/%d/%Y")
        t = time.localtime()
        current_time = time.strftime("%I:%M", t)
        timeformat = '%I:%M'
    for instance in qr_staff:
        status = instance.status
        id = instance.id
        official = instance.current_official_outpass_id
        personal = instance.current_personal_outpass_id

        # * Approved Entry Official Outpass (Check Out)
        if status == 2 and personal == 0 and official != 0:
            outpass_locator_staff_details.objects.filter(id=id).update(status=3)
            official_outpass_locator_logs.objects.filter(id=official).update(
                inclusive_dates         =           current_date,
                time_check_out          =           current_time,
                if_approved             =           1,
                month                   =           current_month      
            )
        
        # * Approved Entry Personal Outpass (Check Out)
        elif status == 2 and official == 0 and personal != 0:
            outpass_locator_staff_details.objects.filter(id=id).update(status=3)
            outpass_locator_logs.objects.filter(id=personal).update(
                inclusive_dates         =           current_date,
                time_check_out          =           current_time,
                if_approved             =           1,
                month                   =           current_month 
            )
        
        # * Approved Entry Official Outpass (Check In)
        elif status == 3 and personal == 0 and official != 0:
            official_outpass_locator_data = official_outpass_locator_logs.objects.filter(id=official)
            for official_outpass_data in official_outpass_locator_data:
                official_check_out = official_outpass_data.time_check_out
                official_time_used = datetime.strptime(current_time, timeformat) - datetime.strptime(official_check_out, timeformat)
                official_outpass_locator_logs.objects.filter(id=official).update(time_check_in=current_time)
                official_outpass_locator_logs.objects.filter(id=official).update(time_span_outpass=official_time_used)

                outpass_locator_staff_details.objects.filter(id=id).update(current_official_outpass_id=0)
                outpass_locator_staff_details.objects.filter(id=id).update(status=1)

        
        # * Approved Entry Personal Outpass (Check In)
        elif status == 3 and official == 0 and personal != 0:
            personal_outpass_locator_data = outpass_locator_logs.objects.filter(id=personal)
            for personal_outpass_data in personal_outpass_locator_data:
                personal_check_out = personal_outpass_data.time_check_out
                personal_time_used = datetime.strptime(current_time, timeformat) - datetime.strptime(personal_check_out, timeformat)
                outpass_locator_logs.objects.filter(id=personal).update(time_check_in=current_time)
                outpass_locator_logs.objects.filter(id=personal).update(time_span_outpass=personal_time_used)

                outpass_locator_staff_details.objects.filter(id=id).update(current_personal_outpass_id=0)
                outpass_locator_staff_details.objects.filter(id=id).update(status=1)

        

        # * IF Staff is on RSO
        elif status == 4 and personal == 0 and official == 0:
            messages.error(request, 'Staff is on RSO!')
        

        # * IF Staff is on Travel
        elif status == 5 and personal == 0 and official == 0:
            messages.error(request, 'Staff is on Travel!')
        

        # * IF Staff is on Leave
        elif status == 6 and personal == 0 and official == 0:
            messages.error(request, 'Staff is on Leave!')




        return redirect('staff_details')


@login_required
def update_remarks_official_outpass(request):

    if request.method == "POST":

        id = request.POST.get('outpass_id')

        official_outpass_locator_logs.objects.filter(id=id).update(
            remarks         =       request.POST.get('remarks'),
            place_visited   =       request.POST.get('destination')
        )

        return redirect('program_outpass_logs')


@login_required
def view_remarks_official(request,pk):
    if pk is not None:

        remarks = official_outpass_locator_logs.objects.all().extra(
            select = {'id': 'official_outpass_locator_logs.id', 'remarks': 'official_outpass_locator_logs.remarks', 'destination': 'official_outpass_locator_logs.place_visited',
                      'id_number': 'official_outpass_locator_logs.id_number', 'first_name': 'auth_user.first_name', 'last_name': 'auth_user.last_name'},
            tables = ['official_outpass_locator_logs', 'auth_user'],
            where = ['official_outpass_locator_logs.id = '+ pk , 'auth_user.id = official_outpass_locator_logs.user_id'],
        )

        remarks_data = list(remarks.values('first_name','last_name','id_number','remarks','destination', 'id'))
        data = dict()
        data['remarks_data'] = remarks_data

    return JsonResponse(data, safe=False)


@login_required
def print_staff_outpass(request):

    template = "app/pages/monitoring/print_outpass.html"

    # if request.method == "POST":
    #     date = request.POST.get('date_range')
    #     staff_id = request.POST.get('staff_id')



    # date_from = date[0:10]
    # date_to = date[13:23]
    # print_outpass_official = official_outpass_locator_logs.objects.filter(inclusive_dates__range=[date_from,date_to]).filter(outpass_locator_staff_details_id=staff_id)

    # print_outpass_official_data = list(print_outpass_official.values('inclusive_dates','time_check_out','time_check_in'))


    # print_outpass_personal = outpass_locator_logs.objects.filter(inclusive_dates__range=[date_from,date_to]).filter(outpass_locator_staff_details_id=staff_id)

    # print_outpass_personal_data = list(print_outpass_personal.values('inclusive_dates','time_check_out','time_check_in'))


    # result_list = list(chain(print_outpass_official_data,print_outpass_personal_data))

    return render(request,template)




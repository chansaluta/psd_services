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
import numpy as np

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
    on_leave_staff = outpass_locator_staff_details.objects.filter(status=3).count()
    staff_use_outpass = outpass_locator_logs.objects.all().count()

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

    return render(request, template)

@login_required
def today_outpass_logs(request):
    template = "app/pages/outpass_logs/today_outpass_logs.html"

    return render(request, template)

@login_required
def staff_details(request):
    template = "app/pages/monitoring/staff_details.html"

    return render(request, template)

@login_required
def staff_program(request):
    template = "app/pages/monitoring/staff_program.html"

    return render(request, template)

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

    context = {
        'secretariat_staff': secretariat_staff,
        'mta_staff': mta_staff,
        'arrs_staff': arrs_staff,
        'sectoral_staff': sectoral_staff,
        'cbu_staff': cbu_staff,
        'rrptp_staff': rrptp_staff,
        'sfp_staff': sfp_staff,
        'socpen_staff': socpen_staff
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

        auth_user_id = auth_user_register.id,
        id_number = request.POST.get('id_number'),
        first_name = request.POST.get('firstname'),
        middle_name = request.POST.get('middlename'),
        last_name = request.POST.get('lastname'),
        ext_name = request.POST.get('extension'),
        full_name = fullname,
        position = request.POST.get('position'),
        status = 1,
        program =  request.POST.get('section'),
        current_outpass_id = 0,
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
        where=[ 'outpass_locator_staff_details.id = auth_user.id' ]

    )
    all_staff_details_list = list(all_staff_details.values('id','id_number','first_name','middle_name','last_name','ext_name','position','status','program','username','email','image'))

    data = {
        'data': all_staff_details_list
    }

    return JsonResponse(data)



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
        auth_user_id = instance.auth_user_id
        id = instance.id
       

        if status == 1:
            outpass_locator_staff_details.objects.filter(id_number=id_number).update(status=2)
            
            outpass_locator = outpass_locator_logs(
                id_number = id_number,
                user_id = auth_user_id,
                outpass_locator_staff_details_id = id,
                inclusive_dates = current_date,
                time_check_out = current_time,
                month = current_month

            )
            outpass_locator.save()
            
            outpass_locator_staff_details.objects.filter(id_number=id_number).update(current_outpass_id=outpass_locator.id)
        elif status == 2:
            for outpass_intance in qr_staff:
                outpass_locator_id = outpass_intance.current_outpass_id

                outpass_locator_data = outpass_locator_logs.objects.filter(id=outpass_locator_id)

                for outpass_data in outpass_locator_data:
                    check_out = outpass_data.time_check_out
                    time_used = datetime.strptime(current_time, timeformat) - datetime.strptime(check_out, timeformat)

                    outpass_locator_logs.objects.filter(id=outpass_locator_id).update(time_check_in=current_time)
                    outpass_locator_logs.objects.filter(id=outpass_locator_id).update(time_span_outpass=time_used)

                    outpass_locator_staff_details.objects.filter(id_number=id_number).update(current_outpass_id=0)
                    outpass_locator_staff_details.objects.filter(id_number=id_number).update(status=1)
        
        elif status == 3:
            messages.error(request, 'Staff is on leave!')
            
        return redirect('tracker')

    

    return render(request,template)


@login_required
def get_staff_outpass_logs(request):

    staff_outpass_logs = outpass_locator_logs.objects.all().extra(
        select = {'id': 'outpass_locator_logs.id','first_name': 'outpass_locator_staff_details.first_name', 'middle_name': 'outpass_locator_staff_details.middle_name', 'last_name': 'outpass_locator_staff_details.last_name',
        'position': 'outpass_locator_staff_details.position', 'image': 'outpass_locator_staff_details.image', 'program': 'outpass_locator_staff_details.program','inclusive_dates': 'outpass_locator_logs.inclusive_dates',
        'time_check_out': 'outpass_locator_logs.time_check_out', 'time_check_in': 'outpass_locator_logs.time_check_in', 'time_span_outpass': 'outpass_locator_logs.time_span_outpass', 
        'status': 'outpass_locator_staff_details.status', 'month': 'outpass_locator_logs.month', 'full_name': 'outpass_locator_staff_details.full_name'},
        tables=['outpass_locator_logs', 'outpass_locator_staff_details'],
        where=['outpass_locator_logs.outpass_locator_staff_details_id = outpass_locator_staff_details.id']
    )

    staff_outpass_logs_data = list(staff_outpass_logs.values('full_name','month','first_name','middle_name','last_name','position','image','program','inclusive_dates','time_check_out','time_check_in','time_span_outpass','status','id'))

    data = {
        'data': staff_outpass_logs_data
    }

    return JsonResponse(data)



@login_required
def get_staff_outpass_today_logs(request):

    staff_outpass_today_logs = outpass_locator_logs.objects.all().extra(
        select = {'id': 'outpass_locator_logs.id','first_name': 'outpass_locator_staff_details.first_name', 'middle_name': 'outpass_locator_staff_details.middle_name', 'last_name': 'outpass_locator_staff_details.last_name',
        'position': 'outpass_locator_staff_details.position', 'image': 'outpass_locator_staff_details.image', 'program': 'outpass_locator_staff_details.program','inclusive_dates': 'outpass_locator_logs.inclusive_dates',
        'time_check_out': 'outpass_locator_logs.time_check_out', 'time_check_in': 'outpass_locator_logs.time_check_in', 'time_span_outpass': 'outpass_locator_logs.time_span_outpass', 
        'status': 'outpass_locator_staff_details.status', 'full_name': 'outpass_locator_staff_details.full_name'},
        tables=['outpass_locator_logs', 'outpass_locator_staff_details'],
        where=['outpass_locator_logs.outpass_locator_staff_details_id = outpass_locator_staff_details.id', 'outpass_locator_logs.inclusive_dates = "' +date_today+ '"']
    )

    staff_outpass_today_logs_data = list(staff_outpass_today_logs.values('full_name','first_name','middle_name','last_name','position','image','program','inclusive_dates','time_check_out','time_check_in','time_span_outpass','status','id'))

    data = {
        'data': staff_outpass_today_logs_data
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
        where=[ 'outpass_locator_staff_details.id = auth_user.id', 'outpass_locator_staff_details.program = "' + program + '"' ]

    )
    all_staff_details_list = list(all_staff_details.values('id','id_number','first_name','middle_name','last_name','ext_name','position','status','program','username','email','image'))

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
def get_outpass_leaderboard(request):



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
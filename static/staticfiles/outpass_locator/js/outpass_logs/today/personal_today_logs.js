


var staff_personal_outpass_logs_today_table = $('#staff_personal_outpass_today_logs');


staff_personal_outpass_logs_today_table.DataTable( {
    responsive: true,
    
    ajax: {
        url: $('#staff_personal_outpass_today_logs').data('url'),
        contentType: 'application/json; charset=utf-8',
        datatype: 'json',
    
        data: {
            pagination: {
                perpage: 50,
            },
            },
        },
    columns: [
        {data: 'image'},
        {data: 'full_name'},
       {data: 'position'},
       {data: 'program'},
       {data: 'inclusive_dates'},
       {data: 'time_check_out'},
       {data: 'time_check_in'},
       {data: 'time_span_outpass'},
       {data: {id: 'id'},
       title: 'Actions',
       orderable: false,
       render: function(data, type, full, meta) {
        return '\<i class="icofont icofont-ui-settings fs-4"></i>';
       },
    },


    ],
    columnDefs: [
        {
            targets: -2,
            render: function(data,type,full,meta) {
                var time_span = data;
                var new_time_span = '';
                var hours = time_span.slice(0, 1);
                var minutes = time_span.slice(2,4);
                if(hours >= '1') {
                    new_time_span = hours + ' hour/s' + ' and ' + minutes + ' minute/s';
                }
                else {
                    new_time_span = + minutes + ' minute/s';
                }
                return '<a class="badge badge-light text-dark" href="#">'+new_time_span+'</a>'
            }
        },

        {
            targets: -3,
            render: function(data,type,full,meta) {
                var check_in = data;
                var hours = check_in.slice(0,-3);
                var minutes = check_in.slice(3,5);
                var ampm = '';
                if(hours >= '08' && hours <= '11') {
                    ampm = 'am'
                }
                else if(hours == '12' || hours >= '01' && hours <= '05'){
                    ampm = 'pm'
                }
                

                return '<a class="badge badge-success" href="#"><i class="fa fa-sign-in m-r-5"></i>'+hours+':'+minutes+' '+ampm+'</a>'
            }
        },

        {
            targets: -4,
            render: function(data,type,full,meta) {
                var check_out = data;
                var hours = check_out.slice(0,-3)
                var minutes = check_out.slice(3,5);
                var ampm = '';
                if(hours >= '08' && hours <= '11') {
                    ampm = 'am'
                }
                else if(hours == '12' || hours >= '01' && hours <= '05'){
                    ampm = 'pm'
                }
                
             
                return '<a class="badge badge-info" href="#"><i class="fa fa-sign-out m-r-5"></i>'+hours+':'+minutes+' '+ampm+'</a>'
            }
        },
        {
            width: '50px',
            targets: -9,
            render: function(data,type,full,meta) {
                return '<img class="img-fluid img-40 rounded-circle" src="/outpass_locator/media/'+data+'" alt="Image description">'
            },
        },
   
    ],
});



$('#search_employee').change(function(e){
    var key = $(this).val();

    if (key == "") {
        $('#registration_form .id_number').val('');
        $('#registration_form .username').val('');
        $('#registration_form .firstname').val('');
        $('#registration_form .middlename').val('');
        $('#registration_form .lastname').val('');
        $('#registration_form .position').val('');
        $('#registration_form .section').val('');
        $('#registration_form .extension').val('-');
    }

    else {

        $.ajax({
            url: '/outpass_locator/administrator/ajax/employee_list/'+key,
            dataType: 'json',
            type: 'GET',
            contentType: 'application/json; charset=utf-8',
            success: function (response){
                $('#registration_form .id_number').val('');
                $('#registration_form .username').val('');
                $('#registration_form .email').val('');
                $('#registration_form .firstname').val('');
                $('#registration_form .middlename').val('');
                $('#registration_form .lastname').val('');
                $('#registration_form .position').val('');
                $('#registration_form .section').val('');
                    response.todos.forEach(todos => {
                        $('#registration_form .id_number').val(todos.id_number);
                        $('#registration_form .username').val(todos.username);
                        $('#registration_form .firstname').val(todos.first_name);
                        $('#registration_form .middlename').val(todos.middle_name);
                        $('#registration_form .lastname').val(todos.last_name);
                        $('#registration_form .extension').val('-');
                        $('#registration_form .position').val(todos.position);
                        $('#registration_form .section').val(todos.section);
                    });

            },
            error: function(error) {
                $('#registration_form .id_number').val('');
                $('#registration_form .username').val('');
                $('#registration_form .extension').val('-');
                $('#registration_form .firstname').val('');
                $('#registration_form .middlename').val('');
                $('#registration_form .lastname').val('');
                $('#registration_form .position').val('');
                $('#registration_form .section').val('');
            }
            


        });

    }


});


var staff_details_table = $('#all_staff_details')


staff_details_table.DataTable( {
    responsive: true,
    
    ajax: {
        url: $('#all_staff_details').data('url'),
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
        {data: {first_name: 'first_name',  last_name: 'last_name'},
        render: function(data, type, full) {
            return data.first_name +' '+ data.last_name;
        }
       },
       {data: 'position'},
       {data: 'program'},
       {data: 'status'},
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
            width: '50px',
            targets: -6,
            render: function(data,type,full,meta) {
                return '<img class="img-fluid img-40 rounded-circle" src="/outpass_locator/media/'+data+'" alt="Image description">'
            },
        },
        {
            width: '75px',
            targets: -2,
            render: function(data, type,full, meta){
                var status = {
                    1: {'title': 'Active', 'class': 'primary', 'icon': 'fa-check-circle' },
                    2: {'title': 'Outpass', 'class': 'success', 'icon': 'fa-clock-o'},
                    3: {'title': 'On Leave', 'class': 'danger', 'icon': 'fa-share-square-o'},
                    
                };
                if (typeof status[data] === 'undefined') {
                    return data;
                }
                return '<a class="badge badge-'+status[data].class+'" href="#"><i class="fa '+status[data].icon+' m-r-5"></i>'+status[data].title+'</a>'

            },
        },
    ],
});






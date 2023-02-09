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



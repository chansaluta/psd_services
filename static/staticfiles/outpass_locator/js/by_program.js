var staff_details_by_program_table = $('#by_program_staff_details')


staff_details_by_program_table.DataTable( {
    responsive: true,
    
    ajax: {
        url: $('#by_program_staff_details').data('url'),
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
       targets: -1,
       title: 'Actions',
       orderable: false,
       render: function(data, type, full, meta) {
        return '\<i style="cursor:pointer;" onclick="update_status('+data.id+')" class="icofont icofont-ui-settings fs-4"></i>';
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
                return '<a  class="badge badge-'+status[data].class+'" href="#"><i  class="fa '+status[data].icon+' m-r-5"></i>'+status[data].title+'</a>'

            },
        },
    ],
});





function update_status(data) {
    $.ajax({
        url: '/outpass_locator/ajax/staff_status_update/'+data,
        dataType: 'json',
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            response.status_modal_data.forEach(status_modal_data => {
                var firstname = status_modal_data.first_name;
                var lastname = status_modal_data.last_name;

                var fullname = firstname + ' ' + lastname;
                var status = status_modal_data.status;

                $('#staff_status_update .fullname').val(fullname);
                $('#staff_status_update .position').val(status_modal_data.position);
                $('#staff_status_update .id').val(status_modal_data.id);

                if(status == 1){
                    $('#staff_status_update .status').val('1');
                }
                else if(status == 3) {
                    $('#staff_status_update .status').val('3');
                }
                
                

                $('#staff_status_update').modal('show');

            
               
            });
           
        },
        error: function(response) {
            console.log(response.responseJSON.errors);
        }

    });
}
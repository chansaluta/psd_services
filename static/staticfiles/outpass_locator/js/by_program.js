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
       {data: {id: 'id',qr_code: 'qr_code'},
       targets: -1,
       title: 'Actions',
       orderable: false,
       render: function(data, type, full, meta) {
        return '<i style="cursor:pointer;" onclick="update_status('+data.id+')"  class="fa fa-gear fs-4 me-2"></i>'+
               '<i style="cursor:pointer;" onclick="update_outpass('+data.id+')" class="fa fa-history fs-4 me-2"></i>'+
               '<a href="/outpass_locator/media/'+data.qr_code+'"  download="/outpass_locator/media/'+data.qr_code+'"><i style="cursor:pointer;"  class="fa fa-download fs-4 me-2" ></i></a>'+
               '<i style="cursor:pointer;" onclick="print_outpass('+data.id+')" class="fa fa-print fs-4"></i>';
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
                    1: {'title': 'Office', 'class': 'primary', 'icon': 'fa-desktop' },
                    2: {'title': 'Outpass', 'class': 'info', 'icon': 'fa-check-square' },
                    3: {'title': 'Outpass Approved', 'class': 'success', 'icon': 'fa-clock-o'},
                    4: {'title': 'RSO', 'class': 'danger', 'icon': 'fa-suitcase'},
                    5: {'title': 'Travel', 'class': 'danger', 'icon': 'fa-plane'},
                    6: {'title': 'On Leave', 'class': 'danger', 'icon': 'fa-share-square-o'},
                    
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





function update_outpass(data) {
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

                $('#staff_outpass_update .fullname').val(fullname);
                $('#staff_outpass_update .position').val(status_modal_data.position);
                $('#staff_outpass_update .id').val(status_modal_data.id);

                if(status == 1){
                    $('#staff_outpass_update .status').val('1');
                }
                else if(status == 3) {
                    $('#staff_outpass_update .status').val('3');
                }
                
                

                $('#staff_outpass_update').modal('show');

            
               
            });
           
        },
        error: function(response) {
            console.log(response.responseJSON.errors);
        }

    });
}



function print_outpass(data) {
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


                $('#print_outpass .fullname').val(fullname);
                $('#print_outpass .position').val(status_modal_data.position);

                $('#print_outpass .id').val(status_modal_data.id);
               

             
           
                

                $('#print_outpass').modal('show');

            
               
            });
           
        },
        error: function(response) {
            console.log(response.responseJSON.errors);
        }

    });
        

}
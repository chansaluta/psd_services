
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
        return '\<i style="cursor:pointer;" onclick="approved_outpass('+data.id+')" class="icofont icofont-ui-settings fs-4"></i>';
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
                return '<a class="badge badge-'+status[data].class+'" href="#"><i class="fa '+status[data].icon+' m-r-5"></i>'+status[data].title+'</a>'

            },
        },
    ],
});






function approved_outpass(data) {
    $.ajax({
        url: '/outpass_locator/ajax/staff_status_update/'+data,
        dataType: 'json',
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
            response.status_modal_data.forEach(status_modal_data => {
                var firstname = status_modal_data.first_name;
                var lastname = status_modal_data.last_name;

                var id_number = status_modal_data.id_number;

                var fullname = firstname + ' ' + lastname;
                var status = status_modal_data.status;

                $('#approved_outpass .fullname').val(fullname);
                $('#approved_outpass .position').val(status_modal_data.position);
                $('#approved_outpass .id').val(status_modal_data.id);

                $('#approved_outpass .id_number').val(id_number);

                if(status == 1){
                    $('#approved_outpass .status').val('1');
                }
                else if(status == 3) {
                    $('#approved_outpass .status').val('3');
                }
                
                

                $('#approved_outpass').modal('show');

            
               
            });
           
        },
        error: function(response) {
            console.log(response.responseJSON.errors);
        }

    });
}

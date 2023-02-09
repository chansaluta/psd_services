"use strict";

var OfficialAdvanceFilterDatatable = function() {

    $.fn.dataTable.Api.register('column().title()', function() {
		return $(this.header()).text().trim();
	});

    


    var OfficialinitTableOutpass = function() {

    var staff_official_outpass_logs_table = $('#staff_official_outpass_logs').DataTable({
    responsive: true,
    processing: true,
    serverPaging: true,
    serverFiltering: true,
    pageSize: 10,
    serverSorting: true,
    ajax: {
        url: $('#staff_official_outpass_logs').data('url'),
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
       {data: 'month'},
       {data: 'destination'},
       {data: 'remarks'},
       {data: 'Actions', responsivePriority: 0 },


    ],

    


    initComplete: function() {
        this.api().columns().every(function() {
            var column = this;

            switch (column.title()) {
                
                case 'Name':
                    column.data().unique().sort().each(function(d, j) {
                        $('.datatable-input-official[data-col-index="1"]').append('<option value="' + d + '">' + d + '</option>');
                    });
                    break;
                
                case 'Month':
                            column.data().unique().sort().each(function(d, j) {
                                $('.datatable-input-official[data-col-index="8"]').append('<option value="' + d + '">' + d + '</option>');
                            });
                            break;

               
                
               

            
            }
        });


    
    
    },


    columnDefs: [
        {
            targets: 8,
            render: function(data,type,full,meta) {
                var month = data;
                return ''+month+'';
            }
        },
        
      
            {
            targets: 11,
            title: 'Actions',
            orderable: false,
                render: function(data, type, full, meta) {
                    return '\<i class="icofont icofont-ui-settings fs-4"></i>';
         },
        },
        {
            targets: 7,
            render: function(data,type,full,meta) {
                var time_span = data;
                var new_time_span = '';
                var hours = time_span.slice(0,1);
                var minutes = time_span.slice(2,4);
                if(hours >= 1) {
                    new_time_span = hours + ' hour/s' + ' and ' + minutes + ' minute/s';
                }
                else {
                    new_time_span = + minutes + ' minute/s';
                }
                return '<a class="badge badge-light text-dark" href="#">'+new_time_span+'</a>'
            }
        },

        {
            targets: 6,
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
            targets: 5,
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
            width: '20px',
            targets: 0,
            render: function(data,type,full,meta) {
                return '<img class="img-fluid img-40 rounded-circle" src="/outpass_locator/media/'+data+'" alt="Image description">'
            },
        },
     
    ],
});



$('#outpass_search_official').on('click', function(e) {
    e.preventDefault();
    var params = {};
    
 
    

    $('.datatable-input-official').each(function() {
        var i = $(this).data('col-index');
        if (params[i]) {
            params[i] += '|' + $(this).val();
            
        }
        else {
            params[i] = $(this).val();
           
        }
    });
    $.each(params, function(i, val) {
        // apply search params to datatable
        staff_official_outpass_logs_table.column(i).search(val ? val : '', false, false);
    });
    staff_official_outpass_logs_table.table().draw();
});

$('#outpass_reset_official').on('click', function(e) {
			e.preventDefault();
			$('.datatable-input-official').each(function() {
				$(this).val('');
				staff_official_outpass_logs_table.column($(this).data('col-index')).search('', false, false);
			});
			staff_official_outpass_logs_table.table().draw();
		});

$('#disabled-days-official').on('keydown', function (e) {
    e.preventDefault();

    var date = $('#advance_filter_outpass_official .outpass_dates_official').val();
    var outpass_date_from = date.substring(0,10);
    var outpass_date_to = date.substring(13,23);
    

    if(date != null) {
    console.log(outpass_date_from);
    console.log(outpass_date_to);
    
 
    staff_official_outpass_logs_table.column(4).search(outpass_date_from && outpass_date_to , true, true);
    }
    staff_official_outpass_logs_table.table().draw();
    // staff_outpass_logs_table.table().draw();
        
});


};

return {
    init: function() {
        OfficialinitTableOutpass();
    },

};


}();

jQuery(document).ready(function() {
	OfficialAdvanceFilterDatatable.init();
});






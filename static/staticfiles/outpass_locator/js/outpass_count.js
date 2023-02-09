display_personal_outpass_leaderboard();
display_official_outpass_leaderboard();

function display_personal_outpass_leaderboard() {
    $('#personal_outpass_leaderboard_tbody').empty();

    $.ajax({
        url: '/outpass_locator/ajax/get_personal_outpass_leaderboard',
        dataType: 'json',
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
           

            

            response.forEach(function(element,index) {
             
                var str = '';

               

                
                str += '<tr>'+
                '<th scope="row">'+(index+1)+'</th>'+
                '<td><img class="img-fluid img-40 rounded-circle" src="/outpass_locator/media/'+element.image+'" alt="Image description"</td>'+
                '<td>'+element.full_name+'</td>'+
                '<td>'+element.id_number+'</td>'+
                '<td>'+element.outpass_count+'</td>'+
                '</tr>';
                $('#personal_outpass_leaderboard_tbody').append(str);

            });
        }

    });
}



function display_official_outpass_leaderboard() {
    $('#official_outpass_leaderboard_tbody').empty();

    $.ajax({
        url: '/outpass_locator/ajax/get_official_outpass_leaderboard',
        dataType: 'json',
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function (response) {
           

            

            response.forEach(function(element,index) {
             
                var str = '';

               

                
                str += '<tr>'+
                '<th scope="row">'+(index+1)+'</th>'+
                '<td><img class="img-fluid img-40 rounded-circle" src="/outpass_locator/media/'+element.image+'" alt="Image description"</td>'+
                '<td>'+element.full_name+'</td>'+
                '<td>'+element.id_number+'</td>'+
                '<td>'+element.outpass_count+'</td>'+
                '</tr>';
                $('#official_outpass_leaderboard_tbody').append(str);

            });
        }

    });
}
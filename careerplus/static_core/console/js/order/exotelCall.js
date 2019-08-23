function makeCallBtn(id) {
 $('#' + id + 'callingBtn').attr('disabled',true)
$('#' + id +'callingbtn-error').css('visibility','hidden');
$('#' + id + 'callingBtn').attr('title','');


    if (id) {
        queue = $('#queueName').val();
        if (!queue){
        queue = "";
        }
        $('#' + id + 'callingBtn').css('color','orange');
        $.ajax({
            type: 'post',
            url: '/ajax/service-call/',
            data: {
                'o_id': id,
                'queue_name':queue
            },
            success: function(response) {
                if (response.status == 1) {
                    $('#' + id + 'callingBtn').css("color",'#008000');
                    $('#' + id + 'callingBtn').attr('disabled',true)
                    $('#' + id +'callingbtn-error').text(response.msg);
                    $('#' + id +'callingbtn-error').css('color','green');
                    $('#' + id +'callingbtn-error').css('visibility','visible');
                    $('#' + id + 'callingBtn').attr('title',response.msg);

                } else {
                  if(response.status == 2){
                    $('#' + id + 'callingBtn').attr('disabled',true)
                     $('#' + id + 'callingBtn').attr('title',response.msg);
                      $('#' + id + 'callingBtn').css('color','red');
                      $('#' + id +'callingbtn-error').text(response.msg);
                        $('#' + id +'callingbtn-error').css('visibility','visible');
                         $('#' + id +'callingbtn-error').css('color','red');
                        fetchReason(id);
                    }
                    else{
                     $('#' + id + 'callingBtn').removeAttr('disabled')
                    $('#' + id + 'callingBtn').css('color','red');
                        $('#' + id +'callingbtn-error').css('visibility','visible');

                       $('#' + id + 'callingBtn').attr('title',response.msg);
                       }

                }
            }
        })
    }
    return false;
}
//this is calling again the welcomeserviceview to get the in case of getting response 403
function fetchReason(id){
   queue = $('#queueName').val();
        if (!queue){
        queue = "";
        }
 if (id) {
        $.ajax({
            type: 'post',
            url: '/ajax/service-call/',
            data: {
                'action': id,'o_id': id,'queue_name':queue,
            },      success: function(response) {
                 $('#' + id + 'callingBtn').removeAttr('disabled')
                 $('#' + id + 'callingBtn').attr('title',response.msg);
                 $('#' + id +'callingbtn-error').text(response.msg);
                 $('#' + id +'callingbtn-error').css('color','red');
                 $('#' + id + 'callingBtn').css('color','red');
            }
        })
    }
    return false;


}
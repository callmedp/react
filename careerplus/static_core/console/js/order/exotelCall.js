function makeCallBtn(id) {
 $('#' + id + 'callingBtn').attr('disabled',true)
    if (id) {
        $('#' + id + 'callingBtn').css('color','orange');
        $.ajax({
            type: 'post',
            url: '/ajax/service-call/',
            data: {
                'o_id': id
            },
            success: function(response) {
                if (response.status == 1) {
                    $('#' + id + 'callingBtn').css("color","green");
                    $('#' + id + 'callingBtn').attr('disabled',true)

                     $('#' + id + 'callingBtn').attr('title',response.msg);

                } else {
                     $('#' + id + 'callingBtn').removeAttr('disabled')
                    $('#' + id + 'callingBtn').css('color','red');
                       $('#' + id + 'callingBtn').attr('title',response.msg);

                }
            }
        })
    }
    return false;
}

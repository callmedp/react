$(function(){

    $('#action_button_go').click(function(){
        var action = $('#id_action').val();
        if (action == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_button').hide();
            $('#actionModal').modal("show");
        }
        else{
            var selected = new Array();
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('value'));
            });

            if (selected.length > 0){
                $('#myModalbody').html('<div class="alert alert-success"> Are you sure to selected  '+ selected.length +' orderitems to do action' + ' ?</div>');
                $('#action_button').show();
                $('#actionModal').modal("show");
            }
            else{
                $('#myModalbody').html('<div class="alert alert-danger">Please select orderitems first to do actions.</div>');
                $('#action_button').hide();
                $('#actionModal').modal("show");
            }
            
        }

    });


    $('#action_button').click(function(){
        var action = $('#id_action').val();
        if (action == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_button').hide();
            $('#actionModal').modal("show");
        }
        else{
            var selected = [];
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('value'));
            });

            if (selected.length > 0){
                $('#actionModal').modal("hide");
                $('#selected-id').val(JSON.stringify(selected));
                $('#action_form').submit();
            }
            else{
                $('#myModalbody').html('<div class="alert alert-danger">You have selected no orderitem, Please select orderitems first.</div>');
                $('#action_button').hide();
                $('#actionModal').modal("show");
            } 
        }
      
    });

});

function jobProfileUpdate(oi_id, ){
    
    if($('#'+oi_id+'_username').val()=="" || $('#'+oi_id+'_password').val()=="" || $('#'+oi_id+'_flag').is(":not(:checked)"))
        {
            alert('Please fill the required details.');
        }

    else{
        var formData = $('#pro_update' + oi_id).serialize();
        var formAction = $('#pro_update' + oi_id).attr('action');
        user = $('#'+oi_id+'_username').val();
        pass = $('#'+oi_id+'_password').val();
        $('#user' + oi_id).attr('value', user);
        $('#pass' + oi_id).attr('value', pass);
        $.ajax({
            url: formAction,
            type: "POST",
            data : formData,
            dataType: 'json',
            success: function(data){
                if (data['success']==true){
                 alert('Value Updated');
                 location.reload();   
                }
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });
    }
};
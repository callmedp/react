$(function(){

	$('#action_button_go').click(function(){
		var action_type = $('#id_action').val();		
		if (action_type == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_comment').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#commant-table input:checked').each(function() {
                selected.push($(this).prop('name'));
            });
            if (selected.length > 0){
            	$('#myModalbody').html('<div class="alert alert-success"> Are you sure to selected  '+ 'comments' +' to do action' + ' ?</div>');
                $('#action_comment').show();
                $('#actionModal').modal("show");
            	console.log(selected);
	            console.log(selected.length);
            }
            else{
            	$('#myModalbody').html('<div class="alert alert-danger">Please select comments first.</div>');
	            $('#action_comment').hide();
	            $('#actionModal').modal("show");

            }
            
        }

	});


	$('#action_comment').click(function(){
        var action = $('#id_action').val();

        $('#action_type_id').val(action);

        
        if (action == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_comment').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#commant-table input:checked').each(function() {
                selected.push($(this).prop('name'));
            });

            if (selected.length > 0){
            	$("#comment_table_form").submit();
            	$('#actionModal').modal("hide");
                // var formData = $("#comment_table_form").serialize();
                // $.ajax({
                //     url : "/useraccount/user-action/",
                //     type: "POST",
                //     data : formData,
                //     success: function(data, textStatus, jqXHR)
                //     {
                //         window.location.reload();
                //     },
                //     error: function (jqXHR, textStatus, errorThrown)
                //     {
                //         window.location.reload(); 
                //     }
                // });

                // $('#action_user').prop('disabled', true);
                // $('#actionModal').modal("hide");

                     
            }
            else{
                $('#myModalbody').html('<div class="alert alert-danger">You have selected no comments, Please select comments first.</div>');
	            $('#action_user').hide();
	            $('#actionModal').modal("show");
            } 
        }
        

      
    });

});
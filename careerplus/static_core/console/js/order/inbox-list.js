$(function(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

	$('#action_button_go').click(function(){
		var action_type = $('#id_action').val();
		if (!action_type){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_inbox').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#body-table-inbox input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('value'));
            });

            if (selected.length > 0){
            	$('#myModalbody').html('<div class="alert alert-success"> Are you sure to selected '+ selected.length +' order items to do action' + ' ?</div>');
                $('#action_inbox').show();
                $('#actionModal').modal("show");
            }
            else{
            	$('#myModalbody').html('<div class="alert alert-danger">Please select element first to do actions.</div>');
	            $('#action_inbox').hide();
	            $('#actionModal').modal("show");
            }
            
        }

	});


	$('#action_inbox').click(function(){
        var action = $('#id_action').val();
        if (action == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_inbox').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#body-table-inbox input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('value'));
            });

            if (selected.length > 0){
                $('#myModalbody').html('<div class="alert alert-success">Assignment Actions are happening...</div>');
            	$('#action_inbox').hide();
                $.ajax({
                    url: '/console/queue/inbox/',
                    type: "POST",
                    data : {"selected_id": selected, "action_type": action},
                    dataType: 'json',
                    success: function(data) {
                        $('#actionModal').modal("hide");
                        var message = data.display_message
                        alert(message);
                        window.location.reload();
                    },
                    error: function(xhr, ajaxOptions, thrownError) {
                        alert("Something went wrong. Try again later");
                    }
                });

            }
            else{
                $('#myModalbody').html('<div class="alert alert-danger">You have selected no orderitem, Please select orderitems first.</div>');
	            $('#action_inbox').hide();
	            $('#actionModal').modal("show");
            } 
        }
        

      
    });


});
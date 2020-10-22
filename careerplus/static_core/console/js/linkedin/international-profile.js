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


    $('#assignment_button_go').click(function(){
        var action = $('#id_assign_to').val();
        if (action == 0){
            $('#assignmentModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#assignment_action_yes').hide();
            $('#assignmentModal').modal("show");
        }
        else{
            var selected = new Array();
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('value'));
            });

            if (selected.length > 0){
                $('#assignmentModalbody').html('<div class="alert alert-success"> Are you sure to selected  '+ selected.length +' orderitems to assign' + ' ?</div>');
                $('#assignment_action_yes').show();
                $('#assignmentModal').modal("show");
            }
            else{
                $('#assignmentModalbody').html('<div class="alert alert-danger">Please select orderitems first to do actions.</div>');
                $('#assignment_action_yes').hide();
                $('#assignmentModal').modal("show");
            }
            
        }

    });


    $('#assignment_action_yes').click(function(){
        var action = $('#id_assign_to').val();
        if (action == 0){
            $('#assignmentModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#assignment_action_yes').hide();
            $('#assignmentModal').modal("show");
        }
        else{
            var selected = [];
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('value'));
            });

            if (selected.length > 0){
                $('#assignmentModalbody').modal("hide");
                $('#selected-id-assign').val(JSON.stringify(selected));
                $('#assignment_form').submit();
            }
            else{
                $('#assignmentModalbody').html('<div class="alert alert-danger">You have selected no orderitem, Please select orderitems first.</div>');
                $('#assignment_action_yes').hide();
                $('#assignmentModal').modal("show");
            } 
        }
      
    });

});

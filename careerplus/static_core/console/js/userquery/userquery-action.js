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
            	$('#myModalbody').html('<div class="alert alert-success"> Are you sure to selected  '+ selected.length +' leads to do action' + ' ?</div>');
                $('#action_button').show();
                $('#actionModal').modal("show");
            }
            else{
            	$('#myModalbody').html('<div class="alert alert-danger">Please select leads first to do actions.</div>');
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
                $('#myModalbody').html('<div class="alert alert-danger">You have selected no leads, Please select leads first.</div>');
	            $('#action_button').hide();
	            $('#actionModal').modal("show");
            } 
        }
      
    });
});
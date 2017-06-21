$(function(){

	$('#action_button_go').click(function(){
		var action_type = $('#id_action').val();
		if (!action_type){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_inbox').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#inbox-table input:checked').each(function() {
                selected.push($(this).prop('name'));
            });

            if ((selected.length - 1) > 0){
            	$('#myModalbody').html('<div class="alert alert-success"> Are you sure to selected  '+ (selected.length - 1) +' order items to do action' + ' ?</div>');
                $('#action_inbox').show();
                $('#actionModal').modal("show");
            }
            else{
            	$('#myModalbody').html('<div class="alert alert-danger">Please select writer first.</div>');
	            $('#action_inbox').hide();
	            $('#actionModal').modal("show");
            }
            
        }

	});


	$('#action_inbox').click(function(){
        var action = $('#id_action').val();

        $('#action_type_id').val(action);

        
        if (action == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_inbox').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#inbox-table input:checked').each(function() {
                selected.push($(this).prop('name'));
            });

            if ((selected.length -1) > 0){
            	$("#inbox_table_form").submit();
            	$('#actionModal').modal("hide");
            }
            else{
                $('#myModalbody').html('<div class="alert alert-danger">You have selected no orderitem, Please select orderitems first.</div>');
	            $('#action_inbox').hide();
	            $('#actionModal').modal("show");
            } 
        }
        

      
    });

});
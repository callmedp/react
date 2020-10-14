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
            $('#body-table-comment input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('name'));
            });
//            console.log(selected.length);
            if (selected.length > 0){
            	$('#myModalbody').html('<div class="alert alert-success"> Are you sure to selected '+ selected.length + ' comments' +' to do action' + ' ?</div>');
                $('#action_comment').show();
                $('#actionModal').modal("show");
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
            $('#body-table-comment input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('name'));
            });

            if (selected.length > 0){
            	$("#comment_table_form").submit();
            	$('#actionModal').modal("hide");
            }
            else{
                $('#myModalbody').html('<div class="alert alert-danger">You have selected no comments, Please select comments first.</div>');
	            $('#action_comment').hide();
	            $('#actionModal').modal("show");
            } 
        }
        

      
    });

});
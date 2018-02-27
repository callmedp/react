$(function(){

	$('#action_button_go').click(function(){
		var action_type = $('#id_action').val();
        console.log(action_type);
		if (action_type == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_welcome').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('name'));
            });

            if ( selected.length > 0){
            	$('#myModalbody').html('<div class="alert alert-success"> Are you sure to selected ' + selected.length + ' orders to do action' + ' ?</div>');
                $('#action_welcome').show();
                $('#actionModal').modal("show");
            }
            else{
            	$('#myModalbody').html('<div class="alert alert-danger">Please select order id first.</div>');
	            $('#action_welcome').hide();
	            $('#actionModal').modal("show");

            }
            
        }

	});


	$('#action_welcome').click(function(){
        var action = $('#id_action').val();

        $('#action_type_id').val(action);

        
        if (action == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_welcome').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#body-table-list input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('name'));
            });

            if (selected.length > 0){
            	$("#welcome_table_form").submit();
            	$('#actionModal').modal("hide");
            }
            else{
                $('#myModalbody').html('<div class="alert alert-danger">You have selected no orders id, Please select orders first.</div>');
	            $('#action_welcome').hide();
	            $('#actionModal').modal("show");
            } 
        }
    });


    $(document).on('change', '#id-cat', function(){
        var select = $('#id-subcat');
        select.empty();
        select.append("<option value='-1'>Select SubCategory</option>");
        var parent = $(this).val(); 
        switch(parent){ 
            case '21':{
                $("#sub_cat1 option").each(function()
                {
                    select.append("<option value="+ $(this).val()+ ">" + $(this).text() + "</option>");
                });
                break;
            }
            case '22':{
                $("#sub_cat2 option").each(function()
                {
                    select.append("<option value="+ $(this).val()+ ">" + $(this).text() + "</option>");
                });
                break;
            }
            case '23':{
                $("#sub_cat3 option").each(function()
                {
                    select.append("<option value="+ $(this).val()+ ">" + $(this).text() + "</option>");
                });
                break;
            }  
            default: //default child option is blank
                break;
            }
    });

});
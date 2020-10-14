$(function(){

	$('#action_button_go').click(function(){
		var action_type = $('#id_action').val();
        console.log(action_type);
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
            	$('#myModalbody').html('<div class="alert alert-success"> Are you sure to selected  '+ selected.length +' order items to do action' + ' ?</div>');
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
            $('#body-table-inbox input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('value'));
            });

            if (selected.length > 0){
                $('#actionModal').modal("hide");
                $.ajax({
                    url: '/console/linkedin/inbox/',
                    type: "POST",
                    data : {"selected_id": selected, "action_type": action},
                    dataType: 'json',
                    success: function(data) {
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


    $('.date-range-picker').daterangepicker({
        autoUpdateInput: false,
        locale: {
          format: 'DD/MM/YYYY',
          cancelLabel: 'Clear',
        },
    },function(start, end, label) {
      
    });

    $('.date-range-picker').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format('DD/MM/YYYY'));
    });

    $('.date-range-picker').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    })

    $('#id_filter').click(function(){
        $('#list-filter-form').submit();
    });
    
    
});
$(function(){

	$('#action_button_go').click(function(){
		var action_type = $('#id_action').val();		
		if (action_type == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_review').hide();
            $('#actionModal').modal("show");
        }
        else{
        	var selected = new Array();
            $('#body-table-review input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('name'));
            });
            console.log(selected.length);
            if (selected.length > 0){
            	$('#myModalbody').html('<div class="alert alert-success"> Are you sure to selected '+ selected.length + ' reviews' +' to do action' + ' ?</div>');
                $('#action_review').show();
                $('#actionModal').modal("show");
            }
            else{
            	$('#myModalbody').html('<div class="alert alert-danger">Please select reviews first.</div>');
	            $('#action_review').hide();
	            $('#actionModal').modal("show");

            }
            
        }

	});

    $('#action_review').click(function(){
        var action = $('#id_action').val();

        $('#action_type_id').val(action);

        
        if (action == 0){
            $('#myModalbody').html('<div class="alert alert-danger">Please select any action first.</div>');
            $('#action_review').hide();
            $('#actionModal').modal("show");
        }
        else{
          var selected = new Array();
            $('#body-table-review input[name="table_records"]:checked').each(function() {
                selected.push($(this).prop('name'));
            });

            if (selected.length > 0){
              $("#review_table_form").submit();
              $('#actionModal').modal("hide");
            }
            else{
                $('#myModalbody').html('<div class="alert alert-danger">You have selected no comments, Please select comments first.</div>');
              $('#action_review').hide();
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
        maxDate: moment().endOf("day"),
    },function(start, end, label) {
      
    });

    $('.date-range-picker').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format('DD/MM/YYYY'));
    });

    $('.date-range-picker').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    })

    $('#review_filter').click(function(){
        $('#review-filter-form').submit();
    });

});
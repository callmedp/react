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

    $('#id_filter').click(function(){
        $('#list-filter-form').submit();
    });

//    $('#downloadReport').click(function(){
//
//                $.ajax({
//                type: "GET",
//                data: {'start_date':$('#id_filter_date').data('daterangepicker').startDate.format('YYYY-MM-DD'),
//                'end_date':$('#id_filter_date').data('daterangepicker').endDate.format('YYYY-MM-DD')}
//                async: false,
//                url:"/ajax/email-exist/",
//                data:{email:$("#id_email").val()},
//                success: function(res)
//                {
//                    emailresponse = !res.exists;
//                }
//            });
//            return emailresponse;
//
//
//    })

});
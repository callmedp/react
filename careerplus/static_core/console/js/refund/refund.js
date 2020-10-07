function totalRefundAmount(){
	var validate_flag = true;
	var checked_items = [];
	var total_refund = 0.0;
    $(".item-checked:checked").each(function() {
        var item_id = this.value;
        var $payment_type_id, $item_id, $refund_amount_id, max_price;
		$payment_type_id = $('#payment-type-id' + item_id);
		$item_id = $('#item-' + item_id);
		$refund_amount_id = $('#refund-amount-id' + item_id);
		max_price = $item_id.attr('data-price');

		try{
            max_price =  parseFloat(max_price);
            if (!max_price){
            	max_price = parseFloat(0.00);
            }
        }
        catch(err){
        	max_price = parseFloat(0.00);
        }
        
        var refund_amount = $refund_amount_id.val();
        var payment_type = $payment_type_id.val();

        try{
            refund_amount =  parseFloat(refund_amount);
            if (refund_amount >= max_price && payment_type == 'partial'){
            	$refund_amount_id.siblings('.error:first').text('value must be less than maximum refund amount');
            	$refund_amount_id.val(refund_amount);
            	validate_flag = false;
            }
            else if(refund_amount < max_price && payment_type == 'partial'){
            	$refund_amount_id.siblings('.error:first').text('');
            	$refund_amount_id.val(refund_amount);
            	total_refund = total_refund + refund_amount;
            }
            else if(refund_amount == 0 && payment_type == 'partial'){
            	$refund_amount_id.siblings('.error:first').text('amount must be greater than zero');
            	validate_flag = false;
            }
            else if(refund_amount == max_price && payment_type == 'full'){
            	$refund_amount_id.siblings('.error:first').text('');
            	$refund_amount_id.val(refund_amount);
            	total_refund = total_refund + refund_amount;
            }
            else if (refund_amount != max_price && payment_type == 'full'){
            	$refund_amount_id.siblings('.error:first').text('this value must be equal to maximum refund amount.');
            	validate_flag = false;
            }
            else if (payment_type == 'select'){
            	$payment_type_id.siblings('.error:first').text('please select valid payment type');
            	validate_flag = false;
            }

            else{
            	$refund_amount_id.siblings('.error:first').text('this value must be float.');
            	validate_flag = false;
            }
        }
        catch(err){
        	$refund_amount_id.siblings('.error:first').text('this value must be float.');
        }
    });
    var $total_refund_amount_id = $('#total-refundable-amount-id');
    total_refund = total_refund.toFixed(2);
    $total_refund_amount_id.text(total_refund);
    $total_refund_amount_id.attr('total-refund', total_refund);
    return validate_flag;
}

function clickItemAction(item_id){
	var $item_id = $('#item-' + item_id);
	if ($item_id.is(':checked')){
		$.ajax({
            url: '/console/refund/validatecheckeditems/',
            type: "GET",
            data : {"item_id": item_id},
            dataType: 'json',
            success: function(data){
            	if (data.status == 1){
            		var $item_id, $payment_type_id, $refund_amount_id;
            		for ( var i = 0, l = data.item_list.length; i < l; i++ ){
            			$item_id = $('#item-' + data.item_list[i]);
            			$item_id.prop('checked', true);

            			$payment_type_id = $('#payment-type-id' + data.item_list[i]);
            			$payment_type_id.val('select');
            			$payment_type_id.siblings('.error:first').text('this value is required.');

            			$refund_amount_id = $('#refund-amount-id' + data.item_list[i]);
            			$refund_amount_id.val('');
					}
					totalRefundAmount();
            	}
            	else if (data.error_message){
            		alert(data.error_message);
            		window.location.reload();
            	}
            	else{
            		alert('Something went wrong. Try again later');
            		window.location.reload();
            	}
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });
	}
	else{
		$.ajax({
            url: '/console/refund/validateuncheckeditems/',
            type: "GET",
            data : {"item_id": item_id},
            dataType: 'json',
            success: function(data){
            	if (data.status == 1){
            		var $item_id, $payment_type_id, $refund_amount_id;
            		for ( var i = 0, l = data.item_list.length; i < l; i++ ){
            			$item_id = $('#item-' + data.item_list[i]);
            			$item_id.prop('checked', false);

            			$payment_type_id = $('#payment-type-id' + data.item_list[i]);
            			$payment_type_id.val('select');
            			$payment_type_id.siblings('.error:first').text('');

            			$refund_amount_id = $('#refund-amount-id' + data.item_list[i]);
            			$refund_amount_id.val('');
					}
					totalRefundAmount();
            	}
            	else if (data.error_message){
            		alert(data.error_message);
            		window.location.reload();
            	}
            	else{
            		alert('Something went wrong. Try again later');
            		window.location.reload();
            	}
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });
	}

	$("#raise-request-submit-id").siblings('.error:first').text('');
}

function changePaymentType(item_id){
	if (item_id){
		var $payment_type_id, $item_id, $refund_amount_id, max_price;
		$payment_type_id = $('#payment-type-id' + item_id);
		$item_id = $('#item-' + item_id);
		max_price = $item_id.attr('data-price');
		$refund_amount_id = $('#refund-amount-id' + item_id);

		try{
            max_price =  parseFloat(max_price);
        }
        catch(err){
        	max_price = parseFloat(0.00);
            console.log(err);
        }

		if ($item_id.is(':checked')){
			if ($payment_type_id.val() == 'select'){
				$refund_amount_id.val('');
				$refund_amount_id.prop("disabled", true);
				$payment_type_id.siblings('.error:first').text('this value is required.');
				$refund_amount_id.siblings('.error:first').text('');
			}
			else if ($payment_type_id.val() == 'full'){
				$refund_amount_id.val(max_price);
				$refund_amount_id.prop("disabled", true);
				$payment_type_id.siblings('.error:first').text('');
				$refund_amount_id.siblings('.error:first').text('');
			}
			else if ($payment_type_id.val() == 'partial'){
				$refund_amount_id.val('');
				$refund_amount_id.prop("disabled", false);
				$payment_type_id.siblings('.error:first').text('');
				$refund_amount_id.siblings('.error:first').text('this value is required.');
			}
		}

		totalRefundAmount();

	}
}

function changeRefundAmount(item_id){
	if (item_id){
		var $refund_amount_id, $item_id, $payment_type_id, max_price;
		$payment_type_id = $('#payment-type-id' + item_id);
		$item_id = $('#item-' + item_id);
		max_price = $item_id.attr('data-price');
		$refund_amount_id = $('#refund-amount-id' + item_id);

		try{
            max_price =  parseFloat(max_price);
        }
        catch(err){
        	max_price = parseFloat(0.00);
            console.log(err);
        }
        if ($item_id.is(':checked')){
        	var refund_amount = $refund_amount_id.val();
        	if (!refund_amount){
        		$refund_amount_id.siblings('.error:first').text('this value is required.');
        	}
        	else{
        		try{
		            refund_amount =  parseFloat(refund_amount);
		            if (refund_amount >= max_price){
		            	$refund_amount_id.siblings('.error:first').text('value must be less than maximum refund amount');
		            	$refund_amount_id.val(refund_amount);
		            }
		            else if(refund_amount == 0){
		            	$refund_amount_id.siblings('.error:first').text('this value must be greater than 0.');
		            	$refund_amount_id.val(refund_amount);
		            }
		            else if(refund_amount < max_price){
		            	$refund_amount_id.siblings('.error:first').text('');
		            	$refund_amount_id.val(refund_amount);
		            }
		            else{
		            	$refund_amount_id.siblings('.error:first').text('this value must be float.');
		            }
		        }
		        catch(err){
		        	$refund_amount_id.siblings('.error:first').text('this value must be float.');
		        }
        	}
        }
        totalRefundAmount();
	}
}


function rejectRequestAction(request_id){
    if (request_id){
        var $rejectmodal = $('#reject-modal' + request_id);
        $('#reject-request-form' + request_id)[0].reset();
        $rejectmodal.modal('show');

        $("#reject-confirm-button" + request_id).on("click", function() {
            $('#reject-request-form' + request_id).submit();
        });
    }
}

function approveRequestAction(request_id){
    if (request_id){
        var $approvemodal = $('#approve-modal' + request_id);
        $('#approve-request-form' + request_id)[0].reset();
        $approvemodal.modal('show');
        //$("#approve-confirm-button" + request_id).prop('disabled', false);

        $("#approve-confirm-button" + request_id).on("click", function() {
            $('#approve-request-form' + request_id).submit();
            //$("#approve-confirm-button" + request_id).prop('disabled', true);
        });
    }
}

function cancelRequestAction(request_id){
    if (request_id){
        var $cancelmodal = $('#cancel-modal' + request_id);
        $('#cancel-request-form' + request_id)[0].reset();
        $cancelmodal.modal('show');
        //$("#approve-confirm-button" + request_id).prop('disabled', false);
        $("#cancel-confirm-button" + request_id).on("click", function() {
            $('#cancel-request-form' + request_id).submit();
            //$("#approve-confirm-button" + request_id).prop('disabled', true);
        });
    }
}


$(document).ready(function(){
	// $(".refund-amount").on("change paste keyup", function() {
	//    console.log($(this).attr('data-id')); 
	// });

	$("#raise-request-submit-id").on("click", function() {
		var checked_flag = false;

	    $(".item-checked:checked").each(function() {
	    	checked_flag = true;
	    });
        
	    if (checked_flag){
	    	var custom_validate = totalRefundAmount();
			var $refund_request_form = $('#refund-request-form');
			$refund_request_form.parsley().validate();
			var parsely_validate = $refund_request_form.parsley().isValid();
			if (custom_validate && parsely_validate){
				$('#confirmModal').modal("show");
			}
	    }
	    else{
	    	$("#raise-request-submit-id").siblings('.error:first').text('select atleast one item to refund');
	    }
		
	});

	$("#action_confirm").on("click", function() {
		var $refund_request_form = $('#refund-request-form');
		$refund_request_form.submit();
	});

});
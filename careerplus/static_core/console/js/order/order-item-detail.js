$(function(){
	$('#message-submit').click(function(){
		$('#message-add-form').parsley().validate();
        if ($('#message-add-form').parsley().isValid()){
        	var formData = $('#message-add-form').serialize();
        	$.ajax({
	            url: '/ajax/orderitem/add-comment/',
	            type: "POST",
	            data : formData,
	            dataType: 'json',
	            success: function(json) {
	            	if (json.status == 1){
	            		$('#message-add-form')[0].reset();
		            	alert('Message added successfully');
		            	window.location.reload();
	            	}
	            	else{
	            		alert("Something went wrong. Try again later");
	            	}
	            },
	            error: function(xhr, ajaxOptions, thrownError) {
	                alert("Something went wrong. Try again later");
	            }
	        });
        }
	});
});


function acceptDraftByAdmin(oi_id, ){
    if (oi_id){
        var formData = $('#accept-reject-form' + oi_id).serialize();
        $.ajax({
            url: '/ajax/orderitem/approve-draft/',
            type: "POST",
            data : formData,
            dataType: 'json',
            success: function(json) {
            	if (json.status == 1){
	            	alert('Approved draft successfully');
	            	window.location.reload();
            	}
            	else{
            		alert("Something went wrong. Try again later");
            	}
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });
    }
};


function rejectDraftByAdmin(oi_id, ){
    if (oi_id){
        var formData = $('#accept-reject-form' + oi_id).serialize();
        $.ajax({
            url: '/ajax/orderitem/reject-draft/',
            type: "POST",
            data : formData,
            dataType: 'json',
            success: function(json) {
            	if (json.status == 1){
	            	alert('Draft rejected successfully');
	            	window.location.reload();
            	}
            	else{
            		alert("Something went wrong. Try again later");
            	}
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });
    }
};
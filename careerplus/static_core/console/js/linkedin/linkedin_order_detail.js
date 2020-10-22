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


// function acceptDraftByAdmin(oi_id, ){
//     if (oi_id){
//         var formData = $('#accept-reject-form' + oi_id).serialize();
//         $.ajax({
//             url: '/ajax/orderitem/approve-draft/',
//             type: "POST",
//             data : formData,
//             dataType: 'json',
//             success: function(json) {
//             	if (json.status == 1){
// 	            	alert('Approved draft successfully');
// 	            	window.location.reload();
//             	}
//             	else{
//             		alert("Something went wrong. Try again later");
//             	}
//             },
//             error: function(xhr, ajaxOptions, thrownError) {
//                 alert("Something went wrong. Try again later");
//             }
//         });
//     }
// };


// function rejectDraftByAdmin(oi_id, ){
//     if (oi_id){
//         var formData = $('#accept-reject-form' + oi_id).serialize();
//         $.ajax({
//             url: '/ajax/orderitem/linkedin-reject-draft/',
//             type: "POST",
//             data : formData,
//             dataType: 'json',
//             success: function(json) {
//             	if (json.status == 1){
// 	            	alert('Draft rejected successfully');
// 	            	window.location.reload();
//             	}
//             	else{
//             		alert("Something went wrong. Try again later");
//             	}
//             },
//             error: function(xhr, ajaxOptions, thrownError) {
//                 alert("Something went wrong. Try again later");
//             }
//         });
//     }
// };


function clickSubmitDraft(oi_id, ){
    if (oi_id){
        $('#draft-upload-form' + oi_id).parsley().validate();
        if ($('#draft-upload-form' + oi_id).parsley().isValid()){
            $('#myModalbody' + oi_id).html('<div class="alert alert-success">Are you sure to upload draft and send for approval???</div>');
            $('#uploadDraftAction' + oi_id).show();
            $('#draftmodal' + oi_id).modal("show");
        }
    }
};


function submitMessage(oi_id, ){
    if (oi_id){
        $('#message-add-form' + oi_id).parsley().validate();
        if ($('#message-add-form' + oi_id).parsley().isValid()){
            var formData = $('#message-add-form' + oi_id).serialize();
            $.ajax({
                url: '/ajax/orderitem/add-comment/',
                type: "POST",
                data : formData,
                dataType: 'json',
                success: function(json) {
                    if (json.status == 1){
                        $('#message-add-form' + oi_id)[0].reset();
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
    }
};


function saveWaitingForInput(oi_id, ){
    if (oi_id){
        $('#waiting-form' + oi_id).parsley().validate();
        if ($('#waiting-form' + oi_id).parsley().isValid()){
            var formData = $('#waiting-form' + oi_id).serialize();
            $.ajax({
                url: '/ajax/orderitem/waiting-input-save/',
                type: "POST",
                data : formData,
                dataType: 'json',
                success: function(json) {
                    alert(json.message);
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong. Try again later");
                }
            });
        }
    }
};


function clickApproveDraft(oi_id, ){
    if (oi_id){
        $('#approveDraftBtn'+oi_id).attr('disabled', true);
        $('#approvemodal'+oi_id).on('hidden.bs.modal', function () {
        onClose(oi_id);
        })

        $('#accept-reject-form' + oi_id).parsley().validate();
        if ($('#accept-reject-form' + oi_id).parsley().isValid()){
            $('#approveModalbody' + oi_id).html('<div class="alert alert-success">Are you sure to approve draft???</div>');
            $('#approveAction' + oi_id).show();
            $('#approvemodal' + oi_id).modal("show");
        }
    }
};


function approveDraftByLinkedinAdmin(oi_id, ){
    if (oi_id){
        var formData = $('#accept-reject-form' + oi_id).serialize();
        $.ajax({
            url: '/ajax/orderitem/linkedin-approve-draft/',
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
                    onClose(oi_id);
                }
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });
    }
};


function clickRejectDraft(oi_id, ){
    if (oi_id){
        $('#rejectDraftBtn'+oi_id).attr('disabled', true);
        $('#rejectmodal'+oi_id).on('hidden.bs.modal', function () {
        onClose(oi_id);
        })
        $('#accept-reject-form' + oi_id).parsley().validate();
        if ($('#accept-reject-form' + oi_id).parsley().isValid()){
            $('#rejectModalbody' + oi_id).html('<div class="alert alert-success">Are you sure to reject draft???</div>');
            $('#rejectAction' + oi_id).show();
            $('#rejectmodal' + oi_id).modal("show");
        }
    }
};


function rejectLinkedinDraftByAdmin(oi_id, ){
    if (oi_id){
        var formData = $('#accept-reject-form' + oi_id).serialize();
        $.ajax({
            url: '/ajax/orderitem/linkedin-reject-draft/',
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
                    onClose(oi_id);
                }
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });
    }
};


function onClose(oi_id){
$('#approveDraftBtn'+oi_id).removeAttr('disabled');
$('#rejectDraftBtn'+oi_id).removeAttr('disabled');
};

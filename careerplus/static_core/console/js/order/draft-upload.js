
function clickSubmitDraft(oi_id, ){
    if (oi_id){
    	$('#draft-upload-form' + oi_id).parsley().validate();
        if ($('#draft-upload-form' + oi_id).parsley().isValid()){
            var flow_type = $('#flow-id' + oi_id).val();
//            console.log(flow_type);
            if (flow_type && (flow_type == 2 || flow_type == 10)){
                $('#myModalbody' + oi_id).html('<div class="alert alert-success">Are you sure to upload document and close orderitem?</div>');
            }
            else if (flow_type && flow_type == 6){
                $('#myModalbody' + oi_id).html('<div class="alert alert-success">Are you sure to upload document?</div>');
            }
            else if (flow_type && flow_type == 'detailpage'){
                $('#myModalbody' + oi_id).html('<div class="alert alert-success">Are you sure to upload document?</div>');
            }
            else{
                $('#myModalbody' + oi_id).html('<div class="alert alert-success">Are you sure to upload draft and send for approval?</div>');
            }
            $('#uploadDraftAction' + oi_id).show();
            $('#draftmodal' + oi_id).modal("show");
        }
    }
};

function uploadDraft(oi_id, ){
    if (oi_id){
        $('#draftmodal' + oi_id).modal("hide");
    	$('#draft-upload-form' + oi_id).parsley().validate();
        if ($('#draft-upload-form' + oi_id).parsley().isValid()){
            var formData = new FormData($('#draft-upload-form' + oi_id)[0]);
            $.ajax({
                url: '/ajax/orderitem/upload-draft/',
                type: "POST",
                cache: false,
                processData: false,
                contentType: false,
                async: false,
                data : formData,
                enctype: "multipart/form-data",
                success: function(json) {
                    //$('#draft-upload-form' + oi_id)[0].reset();
                    var message = json.display_message;
                    alert(message);
                    window.location.reload();

                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong. Try again later");
                     window.location.reload();
                }
            });
        }
    }
};

function detailPageUploadDraft(oi_id, ){
    if (oi_id){
        $('#draftmodal' + oi_id).modal("hide");
        $('#draft-upload-form' + oi_id).parsley().validate();
        if ($('#draft-upload-form' + oi_id).parsley().isValid()){
            var formData = new FormData($('#draft-upload-form' + oi_id)[0]);
            $.ajax({
                url: '/ajax/orderitem/detaii-page-upload-draft/',
                type: "POST",
                cache: false,
                processData: false,
                contentType: false,
                async: false,
                data : formData,
                enctype: "multipart/form-data",
                success: function(json) {
                    //$('#draft-upload-form' + oi_id)[0].reset();
                    var message = json.display_message;
                    alert(message);
                    window.location.reload();

                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong. Try again later");
                     window.location.reload();
                }
            });
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
                         window.location.reload();
                    }
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong. Try again later");
                     window.location.reload();
                }
            });
        }
    }
};


function saveWaitingForInput(oi_id, ){
    if (oi_id){
        $('#waiting-form' + oi_id).parsley().validate();
        var msg = $("#message-add-form"+oi_id+" textarea[name=message]").val();
        $('#msgid').val(msg);
        if (!msg)
        {
            alert("Enter message then click on save button");
        }
        if (msg && $('#waiting-form' + oi_id).parsley().isValid()){
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
                     window.location.reload();
                }
            });
        }
    }
};


function clickApproveDraft(oi_id, ){
    if (oi_id){
        $('#approveDraftBtn').attr('disabled', true);
        $('#accept-reject-form' + oi_id).parsley().validate();
        if ($('#accept-reject-form' + oi_id).parsley().isValid()){
            $('#approveModalbody' + oi_id).html('<div class="alert alert-success">Are you sure to approve draft?</div>');
            $('#approveAction' + oi_id).show();
            $('#approvemodal' + oi_id).modal("show");
        }

    }
};



function approveDraftByAdmin(oi_id, ){
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
                    $('#approveDraftBtn').removeAttr('disabled');
                     window.location.reload();
                }
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
                 window.location.reload();
            }
        });
    }
};


function clickRejectDraft(oi_id, ){
    if (oi_id){
        $('#rejectDraftBtn').attr('disabled', true);
        $('#accept-reject-form' + oi_id).parsley().validate();
        if ($('#accept-reject-form' + oi_id).parsley().isValid()){
            $('#rejectModalbody' + oi_id).html('<div class="alert alert-success">Are you sure to reject draft?</div>');
            $('#rejectAction' + oi_id).show();
            $('#rejectmodal' + oi_id).modal("show");
        }
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
                }
                else{
                    alert("Something went wrong. Try again later");
                }
                window.location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
                window.location.reload();
            }
        });
    }
};

function onClose(){
$('#approveDraftBtn').removeAttr('disabled');
$('#rejectDraftBtn').removeAttr('disabled');
};

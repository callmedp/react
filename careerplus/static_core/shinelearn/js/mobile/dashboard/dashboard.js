$.validator.addMethod("extn", function(value, element) {
    var allowedExtensions = /(\.pdf|\.doc|\.docx)$/i;
    if(value && !allowedExtensions.exec(value)){
        return false;
    }
    else{
        return true;
    }
        
});

$.validator.addMethod("custom_comment",
    function(value, element) {
        if($('#reject-reason').val() && $('#reject-reason').val().trim()){
            return true;
        }
        return false;
});


function mobileRejectService(oi_pk) {
    $("#reject-form-id" + oi_pk).validate({
        rules: {
            comment:{
                required: function(){
                    if($('#uploadBtn').val() == "")
                        return true;
                    else
                        return false;
                },
                custom_comment: true,

            } ,

            reject_file: {
                extn: true,
            }
        },
        messages: {
            comment:{
                required: 'This field is required',
                custom_comment: 'This field is required',
            },
            reject_file: 'only pdf, doc and docx formats are allowed',
        },
        submitHandler: function(form) {                
            return false;
        },

    });

    var flag = $('#reject-form-id' + oi_pk).valid();
    if (flag){
        var formData = new FormData($('#reject-form-id' + oi_pk)[0]);
        $.ajax({
            url: '/dashboard/inbox-rejectservice/',
            type: "POST",
            cache: false,
            processData: false,
            contentType: false,
            async: false,
            data : formData,
            enctype: "multipart/form-data",
            success: function(json) {
                $('#reject-form-id' + oi_pk)[0].reset();
                window.location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong. Try again later");
            }
        });

    }   
};

function mobileAccept(oi_pk){
    if (oi_pk){
        var formData = $('#mobileaccept-form' + oi_pk).serialize();
        console.log(formData);
        $.ajax({
            url: '/dashboard/inbox-acceptservice/',
            type: "POST",
            data : formData,
            dataType: 'json',
            success: function(data) {
                $('.modal').hide();
                window.location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, try after sometimes");
                window.location.reload();
            }
        });
    }
}

function openPopup(el) {
    $('.modal').hide();
    $('#' + el).fadeIn(200);   
}

function closePopup() {
    $('.modal').fadeOut(300);
}
function viewDetailOrderitem(oi_pk, ) {
    if (oi_pk){
        $.ajax({
            url: '/user/dashboard/detail/',
            type: "GET",
            data : {'oi_pk': oi_pk, },
            dataType: 'html',
            success: function(html) {
                $('#right-content-id').html(html);
               // $("#load_more" + article_id).remove();
               // $("#page_comment" + article_id).append(html);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong");
            }
        });
    }
};

function viewCommentOrderitem(oi_pk, ) {
    if (oi_pk){
        $.ajax({
            url: '/user/dashboard/comment/',
            type: "GET",
            data : {'oi_pk': oi_pk, },
            dataType: 'html',
            success: function(html) {
                $('#right-content-id').html(html);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong");
            }
        });
    }
};

function rejectService(oi_pk, ) {
    if (oi_pk){
        $.ajax({
            url: '/user/dashboard/rejectservice/',
            type: "GET",
            data : {'oi_pk': oi_pk, },
            dataType: 'json',
            success: function(data) {
                window.location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, try after sometimes");
            }
        });
    }
};

function acceptService(oi_pk, ) {
    if (oi_pk){
        $.ajax({
            url: '/user/dashboard/acceptservice/',
            type: "GET",
            data : {'oi_pk': oi_pk, },
            dataType: 'json',
            success: function(data) {
                window.location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Something went wrong, try after sometimes");
            }
        });
    }
};



$(document).ready(function(){

    $.validator.addMethod("extnAccept", function(value, element) {
        var fileInput = document.getElementById('file-id');
        var filePath = fileInput.value;
        console.log(filePath);
        var allowedExtensions = /(\.pdf|\.doc|\.docx)$/i;
        if(!allowedExtensions.exec(filePath)){
            return false;
        }
        else{
            return true;
        }
            
    });

    $("#resume-upload-form").validate({
        rules: {
            file:{
                required: true,
                maxlength: 200,
                extnAccept: true,
            },        
        },
        messages:{
            file:{
                required: 'this value is required.',
                maxlength: 'length should be less than 200 characters',
                extnAccept: 'only pdf, doc and docx formats are allowed',
            },
        },
        // highlight: function(element) {
        //     $(element).closest('.input-file').addClass('error');
        // },
        // unhighlight: function(element) {
        //     $(element).closest('.input-file').removeClass('error');
        // },
        // errorPlacement: function(error, element){
        //     $(element).closest('.error-txt').html(error.text());
        // }
    });

    $('#upload-resume-button').click(function(){
        var flag = $("#resume-upload-form").valid();
        if (flag){
            $('#resume-upload-form').submit();
        }
    });

    $.validator.addMethod("custom_message",
        function(value, element) {
            if($('#id_comment').val().trim()){
                return true;
            }
            return false;
    });

    $(document).on('click', '#comment_submit_button', function () {
        $("#user-comment-form").validate({
            rules: {
                comment: {
                    required: true,
                    maxlength: 200,
                    custom_message: true,
                },
            },
            messages: {
                comment: {
                    required: "Message is Mandatory.",
                    maxlength: "Length should be less than 200 characters.",
                    custom_message: "Message is Mandatory.",
                },
            },
            errorPlacement: function(error, element){
                $(element).siblings('.error').html(error.text());
            },

        });
        var flag = $('#user-comment-form').valid();
        console.log(flag);
        if (flag){
            var formData = $('#user-comment-form').serialize();
            $.ajax({
                url: '/user/dashboard/comment/',
                type: 'POST',
                data : formData,
                dataType: 'html',
                success: function(html) {
                    $('#right-content-id').html(html);
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong");
                }
            });
        }
    });


});


